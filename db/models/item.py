from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..base import Base

class Item(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    price = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=func.now())
