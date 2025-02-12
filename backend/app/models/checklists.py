
from typing import List, Optional, ForwardRef
from sqlmodel import SQLModel, Field, Relationship


# Forward reference for Event
Event = ForwardRef("Event")


class Checklist(SQLModel, table=True):
    __tablename__ = "checklist"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    event_id: int = Field(foreign_key="event.id", nullable=False)
    name: str = Field(nullable=False, max_length=255)  # Name of the checklist (e.g., "Event Preparations")
    description: Optional[str] = Field(default=None, max_length=500)  # Optional: checklist description

    # Relationship to checklist items
    items: List["ChecklistItem"] = Relationship(back_populates="checklist")

    # Relationship to the event
    event: Optional["Event"] = Relationship(back_populates="checklists")


class ChecklistItem(SQLModel, table=True):
    __tablename__ = "checklist_item"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    checklist_id: int = Field(foreign_key="checklist.id", nullable=False)
    description: str = Field(nullable=False, max_length=255)  # Description of the checklist item
    is_completed: bool = Field(default=False)  # Tracks whether the task is completed
    order: Optional[int] = Field(default=None)  # Optional: Maintain order of tasks

    # Relationship to the checklist
    checklist: Optional["Checklist"] = Relationship(back_populates="items")
