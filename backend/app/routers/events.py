from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_session
from app.models.events import Event, EventGroup

router = APIRouter(prefix="/event_groups", tags=["Event Groups"])

# Event Group Endpoints

@router.post("/", response_model=EventGroup)
async def create_event_group(event_group: EventGroup, session: AsyncSession = Depends(get_session)):
    session.add(event_group)
    await session.commit()
    await session.refresh(event_group)
    return event_group


@router.get("/", response_model=list[EventGroup])
async def list_event_groups(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(EventGroup))
    event_groups = result.scalars().all()
    return event_groups


@router.get("/{event_group_id}/", response_model=EventGroup)
async def get_event_group(event_group_id: int, session: AsyncSession = Depends(get_session)):
    event_group = await session.get(EventGroup, event_group_id)
    if not event_group:
        raise HTTPException(status_code=404, detail="Event Group not found")
    return event_group


@router.put("/{event_group_id}/", response_model=EventGroup)
async def update_event_group(event_group_id: int, event_group_data: EventGroup, session: AsyncSession = Depends(get_session)):
    event_group = await session.get(EventGroup, event_group_id)
    if not event_group:
        raise HTTPException(status_code=404, detail="Event Group not found")
    for key, value in event_group_data.model_dump(exclude_unset=True).items():
        setattr(event_group, key, value)
    session.add(event_group)
    await session.commit()
    await session.refresh(event_group)
    return event_group


@router.delete("/{event_group_id}/")
async def delete_event_group(event_group_id: int, session: AsyncSession = Depends(get_session)):
    event_group = await session.get(EventGroup, event_group_id)
    if not event_group:
        raise HTTPException(status_code=404, detail="Event Group not found")
    await session.delete(event_group)
    await session.commit()
    return {"message": "Event Group deleted successfully"}

# Event Endpoints

@router.post("/{event_group_id}/events/", response_model=Event)
async def create_event(event_group_id: int, event: Event, session: AsyncSession = Depends(get_session)):
    event.event_group_id = event_group_id
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


@router.get("/{event_group_id}/events/", response_model=list[Event])
async def list_events(event_group_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Event).where(Event.event_group_id == event_group_id))
    events = result.scalars().all()
    return events


@router.get("/{event_group_id}/events/{event_id}/", response_model=Event)
async def get_event(event_group_id: int, event_id: int, session: AsyncSession = Depends(get_session)):
    event = await session.get(Event, event_id)
    if not event or event.event_group_id != event_group_id:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_group_id}/events/{event_id}/", response_model=Event)
async def update_event(event_group_id: int, event_id: int, event_data: Event, session: AsyncSession = Depends(get_session)):
    event = await session.get(Event, event_id)
    if not event or event.event_group_id != event_group_id:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event_data.model_dump(exclude_unset=True).items():
        setattr(event, key, value)
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


@router.delete("/{event_group_id}/events/{event_id}/")
async def delete_event(event_group_id: int, event_id: int, session: AsyncSession = Depends(get_session)):
    event = await session.get(Event, event_id)
    if not event or event.event_group_id != event_group_id:
        raise HTTPException(status_code=404, detail="Event not found")
    await session.delete(event)
    await session.commit()
    return {"message": "Event deleted successfully"}
