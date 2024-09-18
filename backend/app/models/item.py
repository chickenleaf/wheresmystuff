# backend/app/models/item.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class ItemStatus(str, Enum):
    LOST = "lost"
    FOUND = "found"

class ItemBase(BaseModel):
    title: str
    description: str
    category: str
    location: str
    status: ItemStatus
    date: datetime = Field(default_factory=datetime.utcnow)

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True

