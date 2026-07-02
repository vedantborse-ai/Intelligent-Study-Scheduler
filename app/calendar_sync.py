import os
import json
import logging
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from zoneinfo import ZoneInfo
from google.oauth2.credentials import Credentials
from datetime import timedelta, timezone
from dateutil.parser import isoparse
from .models import OAuthCredential

# Setup Logger
logger = logging.getLogger("uvicorn")

IST_TIMEZONE = "Asia/Kolkata"
IST = ZoneInfo(IST_TIMEZONE)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_oauth_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
            }
        },
        scopes=SCOPES,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
    )

def push_to_google_calendar(schedule, credentials):
    if not credentials:
        return []

    created_events = []

    try:
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        service = build("calendar", "v3", credentials=credentials)

        for task in schedule:
            title = task.get("task")
            
            # Ensure datetime is timezone-aware
            start_time = task["start"]
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            start_time = start_time.astimezone(IST)

            end_time = task["end"]
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)
            end_time = end_time.astimezone(IST)

            # Delete old event if it exists to avoid duplicates
            old_event_id = task.get("google_event_id")
            if old_event_id:
                try:
                    service.events().delete(
                        calendarId="primary",
                        eventId=old_event_id
                    ).execute()
                    logger.info(f"Deleted old event: {old_event_id}")
                except Exception as ex:
                    logger.warning(f"Could not delete old event {old_event_id}: {ex}")

            event = {
                "summary": title,
                "description": "Scheduled by SmartSchedule AI Engine",
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": IST_TIMEZONE
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": IST_TIMEZONE
                }
            }

            result = service.events().insert(
                calendarId="primary",
                body=event
            ).execute()

            event_id = result.get("id")

            created_events.append({
                "title": title,
                "event_id": event_id,
                "task_id": task.get("task_id")
            })

        return created_events

    except Exception as e:
        logger.error(f"Calendar Sync Error: {e}")
        return []

def load_credentials_from_db(db):
    try:
        record = db.query(OAuthCredential).first()
        if not record:
            return None

        creds = Credentials(
            token=record.token,
            refresh_token=record.refresh_token,
            token_uri=record.token_uri,
            client_id=record.client_id,
            client_secret=record.client_secret,
            scopes=json.loads(record.scopes),
        )

        # Auto-refresh if token is expired
        if creds.expired and creds.refresh_token:
            try:
                from google.auth.transport.requests import Request as AuthRequest
                creds.refresh(AuthRequest())
                
                # Update SQLite database record with refreshed token
                record.token = creds.token
                if creds.refresh_token:
                    record.refresh_token = creds.refresh_token
                db.commit()
                logger.info("Successfully refreshed and saved Google Calendar token to database")
            except Exception as re:
                logger.error(f"Failed to refresh expired token: {re}")
                # We return the credentials anyway and let it fail gracefully at request time
                
        return creds
    except Exception as e:
        logger.error(f"Error loading credentials from DB: {e}")
        return None