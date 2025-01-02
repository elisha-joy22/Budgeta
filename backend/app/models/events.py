from typing import TYPE_CHECKING, List, Optional, ForwardRef
from datetime import date, datetime, timezone
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel

# Forward references (crucial for circular dependencies)
Invitee = ForwardRef("Invitee")

class Event(SQLModel, table=True):
    __tablename__ = "event"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=150, nullable=False)
    description: Optional[str] = None
    event_date: Optional[date] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    event_group_id: int = Field(foreign_key="event_group.id", nullable=False)

    invitees: List[Invitee] = Relationship(back_populates="event")  # Use forward ref here

class EventGroup(SQLModel, table=True):
    __tablename__ = "event_group"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=150, nullable=False)  # Group name, e.g., Wedding, Conference
    description: Optional[str] = None  # Description of the group
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    # Relationship with Events
    events: List[Event] = Relationship(back_populates="event_group")
