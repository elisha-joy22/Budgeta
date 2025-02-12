from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_session
from app.models.checklists import Checklist,ChecklistItem

router = APIRouter(prefix="/api/checklists", tags="Checklists")


router.post("/", response_model=Checklist)
async def create_checklist(checklist_item: ChecklistItem, session: AsyncSession=Depends(get_session)):
    session.add(checklist_item)
    await session.commit()
    await session.refresh(checklist_item)
    return checklist_item


router.get("/", response_model=Checklist)
async def read_checklist_items(session: AsyncSession=Depends(get_session)):
    result = await session.execute(select(ChecklistItem))
    checklist_items = result.scalars().all()
    return checklist_items

