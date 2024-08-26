from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from db.models import item
from db.models.item import Item
from db.db import get_db
from pydantic import BaseModel
from sqlalchemy.engine.result import Result
from sqlalchemy.future import select

TodoInputView_router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    price: int

@TodoInputView_router.post("/items/")
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    item_dict = item.model_dump() #.dict()の代わり
    db_item = Item(**item_dict)
    
    db.add(db_item)
    await db.commit()
    
    return db_item

@TodoInputView_router.get("/items/")
async def get_items(db: AsyncSession = Depends(get_db)):
    result: Result = await db.execute(select(Item))
    items = result.scalars().all()
    return items
    
