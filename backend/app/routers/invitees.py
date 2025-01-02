from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_session
from app.models.invitees import Invitee, RSVPStatus

router = APIRouter(prefix="/invitees", tags=["Invitees"])


# Create a new invitee
@router.post("/", response_model=Invitee)
async def create_invitee(invitee: Invitee, session: AsyncSession = Depends(get_session)):
    session.add(invitee)
    await session.commit()
    await session.refresh(invitee)
    return invitee


# Get all invitees
@router.get("/", response_model=list[Invitee])
async def read_invitees(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Invitee))
    invitees = result.scalars().all()
    return invitees


# Get a single invitee by ID
@router.get("/{invitee_id}", response_model=Invitee)
async def read_invitee(invitee_id: int, session: AsyncSession = Depends(get_session)):
    invitee = await session.get(Invitee, invitee_id)
    if not invitee:
        raise HTTPException(status_code=404, detail="Invitee not found")
    return invitee


# Update an invitee
@router.put("/{invitee_id}", response_model=Invitee)
async def update_invitee(invitee_id: int, invitee_data: Invitee, session: AsyncSession = Depends(get_session)):
    invitee = await session.get(Invitee, invitee_id)
    if not invitee:
        raise HTTPException(status_code=404, detail="Invitee not found")
    for key, value in invitee_data.dict(exclude_unset=True).items():
        setattr(invitee, key, value)
    session.add(invitee)
    await session.commit()
    await session.refresh(invitee)
    return invitee


# Delete an invitee
@router.delete("/{invitee_id}")
async def delete_invitee(invitee_id: int, session: AsyncSession = Depends(get_session)):
    invitee = await session.get(Invitee, invitee_id)
    if not invitee:
        raise HTTPException(status_code=404, detail="Invitee not found")
    await session.delete(invitee)
    await session.commit()
    return {"message": "Invitee deleted successfully"}
