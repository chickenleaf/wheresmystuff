# backend/app/routers/matches.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.item import Item
from app.utils.auth import get_current_user
from app.services.matching_service import find_matches

router = APIRouter()

@router.get("/{item_id}", response_model=List[Item])
async def get_matches(item_id: str, current_user: dict = Depends(get_current_user)):
    matches = await find_matches(item_id)
    return matches