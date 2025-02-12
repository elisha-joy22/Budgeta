from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional, ForwardRef


Event = ForwardRef("Event") 

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from app.models.events import Event  # Update the path based on your project structure


class RSVPStatus(str, Enum):
    NOT_INVITED = "Not Invited"
    WAITING_REPLY = "Waiting for Reply"
    CONFIRMED = "Confirmed"
    DECLINED = "Regretfully Declined"
    ARRIVED = "Arrived"


class Invitee(SQLModel, table=True):
    __tablename__ = "invitee"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=150, nullable=False)  # Name of the invitee
    contact: str = Field(max_length=150, nullable=False)  # Contact information
    accompanying_guests: Optional[int] = Field(default=0)  # Number of additional guests
    rsvp_status: RSVPStatus = Field(default=RSVPStatus.NOT_INVITED)  # RSVP status

    event_id: int = Field(foreign_key="event.id", nullable=False)  # Foreign key to Event

    event: Event = Relationship(back_populates="invitees")
