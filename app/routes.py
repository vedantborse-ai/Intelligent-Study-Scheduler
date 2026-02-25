print("--- ⚡ LOADING ROUTES.PY (WITH TIMEDELTA FIX) ⚡ ---") # <--- LOOK FOR THIS IN TERMINAL

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta  # <--- THIS IS THE CRITICAL FIX
import json
import logging
import traceback

# Import your modules
from .database import SessionLocal
from .models import Task, OAuthCredential
from .scheduler import generate_schedule
from .ai_engine import ai_decision
from .calendar_sync import push_to_google_calendar, load_credentials_from_db, get_oauth_flow

# Setup Logger
logger = logging.getLogger("uvicorn")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel
class TaskInput(BaseModel):
    title: str
    priority: int
    estimated_hours: int
    deadline: datetime

# --- ROUTES ---

@router.post("/tasks")
def add_task(task: TaskInput, db: Session = Depends(get_db)):
    try:
        task_data = task.dict()
        if isinstance(task_data['deadline'], datetime):
            task_data['deadline'] = task_data['deadline'].isoformat()
            
        new_task = Task(**task_data)
        db.add(new_task)
        db.commit()
        return {"message": "Task added successfully"}
    except Exception as e:
        logger.error(f"Error adding task: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/schedule")
def schedule_tasks(db: Session = Depends(get_db)):
    # 1. Get Tasks
    tasks = db.query(Task).filter(Task.completed == False).all()

    # 2. AI Sorting 
    try:
        if tasks:
            tasks = ai_decision(tasks)
    except Exception as e:
        print(f"AI Sort Error: {e}")
        traceback.print_exc()

    # 3. MANUAL JSON CONVERSION (Fixes the [{}] error)
    response_data = []
    for t in tasks:
        response_data.append({
            "id": t.id,
            "title": t.title,
            "priority": t.priority,
            "estimated_hours": t.estimated_hours,
            "deadline": t.deadline,
            "completed": t.completed,
            "google_event_id": t.google_event_id
        })

    return JSONResponse(content=response_data)

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()

    total = len(tasks)
    completed = len([t for t in tasks if t.completed])
    pending = total - completed
    completion_rate = completed / total if total else 0

    # 🔥 Calculate 7-day streak
    today = datetime.utcnow().date()
    streak = 0

    for i in range(7):
        # This line was crashing. It needs 'timedelta' imported above.
        day = today - timedelta(days=i) 
        
        day_active = False
        for t in tasks:
            if t.completed and t.completed_at:
                if isinstance(t.completed_at, str):
                    c_date = datetime.fromisoformat(t.completed_at).date()
                else:
                    c_date = t.completed_at.date()
                
                if c_date == day:
                    day_active = True
                    break
        
        if day_active:
            streak += 1

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_rate": round(completion_rate, 2),
        "weekly_streak": streak
    }

# --- OAUTH & UTILS ---

@router.get("/oauth/login")
def google_login():
    try:
        flow = get_oauth_flow()
        auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
        return RedirectResponse(auth_url)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/oauth/callback")
def google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        flow = get_oauth_flow()
        flow.fetch_token(authorization_response=str(request.url))
        
        creds_json = flow.credentials.to_json()
        creds_dict = json.loads(creds_json)
        
        existing_user = db.query(OAuthCredential).first()
        if existing_user:
            existing_user.token = creds_dict["token"]
            existing_user.refresh_token = creds_dict.get("refresh_token", existing_user.refresh_token)
            existing_user.token_uri = creds_dict["token_uri"]
            existing_user.client_id = creds_dict["client_id"]
            existing_user.client_secret = creds_dict["client_secret"]
            existing_user.scopes = json.dumps(creds_dict["scopes"])
        else:
            new_creds = OAuthCredential(
                token=creds_dict["token"],
                refresh_token=creds_dict.get("refresh_token"),
                token_uri=creds_dict["token_uri"],
                client_id=creds_dict["client_id"],
                client_secret=creds_dict["client_secret"],
                scopes=json.dumps(creds_dict["scopes"])
            )
            db.add(new_creds)
        db.commit()
        return RedirectResponse("http://localhost:5173?status=success")
    except Exception as e:
        return RedirectResponse(f"http://localhost:5173?error={str(e)}")

# --- REPLACE THESE TWO FUNCTIONS IN app/routes.py ---

@router.patch("/tasks/{task_id}/complete")
def complete_task_patch(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task: return JSONResponse(status_code=404, content={"error": "Not found"})

    # 1. Load Credentials to talk to Google
    credentials = load_credentials_from_db(db)

    # 2. Delete from Google Calendar if it exists there
    if task.google_event_id and credentials:
        try:
            from googleapiclient.discovery import build
            service = build("calendar", "v3", credentials=credentials)
            service.events().delete(
                calendarId="primary",
                eventId=task.google_event_id
            ).execute()
            print(f"🗑️ Deleted Google Event: {task.google_event_id}")
        except Exception as e:
            print(f"⚠️ Google Sync Error (Complete): {e}")

    # 3. Mark as complete in Local DB
    task.completed = True
    task.completed_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Task Completed & Removed from Calendar"}

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task: return JSONResponse(status_code=404, content={"error": "Not found"})

    # 1. Load Credentials
    credentials = load_credentials_from_db(db)

    # 2. Delete from Google Calendar if it exists there
    if task.google_event_id and credentials:
        try:
            from googleapiclient.discovery import build
            service = build("calendar", "v3", credentials=credentials)
            service.events().delete(
                calendarId="primary",
                eventId=task.google_event_id
            ).execute()
            print(f"🗑️ Deleted Google Event: {task.google_event_id}")
        except Exception as e:
            print(f"⚠️ Google Sync Error (Delete): {e}")

    # 3. Delete from Local DB
    db.delete(task)
    db.commit()
    
    return {"message": "Task Deleted form DB & Calendar"}

@router.delete("/tasks")
def clear_all_tasks(db: Session = Depends(get_db)):
    db.query(Task).delete()
    db.commit()
    return {"message": "All deleted"}