from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from db.models import item
from db.models.item import Item
from db.db import get_db
from pydantic import BaseModel
from sqlalchemy.engine.result import Result
from sqlalchemy.future import select
from datetime import date

TodoInputView_router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    deadline: date
    
class ItemUpdate(BaseModel):
    name: str
    deadline: date

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



@TodoInputView_router.put("/items/{item_id}")
async def replace_item(item_id: int, item_data: ItemUpdate, db: AsyncSession = Depends(get_db)):
    #データベースからのデータ取得
    result = await db.execute(select(Item).where(Item.item_id == item_id))
    db_item = result.scalar_one_or_none()
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.name = item_data.name
    db_item.deadline = item_data.deadline
    
    await db.commit()
    
    return db_item


@TodoInputView_router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    # アイテムをデータベースから取得
    result = await db.execute(select(Item).where(Item.item_id == item_id))
    item = result.scalar_one_or_none()

    # アイテムが存在しない場合、404エラーを返す
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # アイテムを削除
    await db.delete(item)
    await db.commit()
    
    return {"message": "Item deleted"}
    
