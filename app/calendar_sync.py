import os
import json
import logging
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from zoneinfo import ZoneInfo
from google.oauth2.credentials import Credentials
from datetime import timedelta
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
            start_time = task["start"].astimezone(IST)
            end_time = task["end"].astimezone(IST)

            event = {
                "summary": title,
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
                "event_id": event_id
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

        return Credentials(
            token=record.token,
            refresh_token=record.refresh_token,
            token_uri=record.token_uri,
            client_id=record.client_id,
            client_secret=record.client_secret,
            scopes=json.loads(record.scopes),
        )
    except Exception as e:
        logger.error(f"Error loading credentials from DB: {e}")
        return None