from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    priority = Column(Integer)
    estimated_hours = Column(Integer)
    deadline = Column(String)
    google_event_id = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)


class OAuthCredential(Base):
    __tablename__ = "oauth_credentials"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    token_uri = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    scopes = Column(Text, nullable=False)
