from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from sqlalchemy.future import select
from sqlalchemy import insert 
from ..db.models.item import Item
from ..db import get_db
from pydantic import BaseModel

TodoInputView_router = APIRouter()


# Pydanticモデルを使って、リクエストボディのバリデーションを行います
class ItemCreate(BaseModel):
    name: str
    price: int
    
    
    
    
@TodoInputView_router.post("/items/")
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    # 新しいItemを作成
    new_item = Item(name=item.name, price=item.price)
    
    # データベースに追加
    db.add(new_item)
    
    # トランザクションをコミット
    try:
        await db.commit()
        await db.refresh(new_item)  # データベースで更新された内容を取得
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail="データの保存に失敗しました")
    
    return new_item
