from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, nullable=False, unique=True, index=True)
    name: Optional[str] = Field(max_length=150)  # Optional name of the user
    profile_picture: Optional[str] = None  # URL to the user's profile picture
    oauth_provider: str = Field(max_length=100, nullable=False)  # e.g., "google", "github"
    oauth_provider_id: str = Field(max_length=255, nullable=False, unique=True)  # Unique ID from the OAuth provider
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    # Relationships
    event_groups: List["EventGroup"] = Relationship(back_populates="user")
