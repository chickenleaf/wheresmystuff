from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
import logging
from app.models.item import Item, ItemCreate
from app.utils.auth import get_current_user
from app.services.mongodb_service import create_item, get_items, get_item, update_item, delete_item
from app.services.elasticsearch_service import search_items
from app.services.celery_tasks import process_item_async

router = APIRouter()
logger = logging.getLogger("lost_and_found")

@router.post("/", response_model=Item)
async def create_new_item(item: ItemCreate, current_user: dict = Depends(get_current_user)):
    try:
        db_item = await create_item(item, current_user["id"])
        process_item_async.delay(str(db_item.id))
        logger.info(f"Item created: {db_item.id}", extra={
            "user_id": current_user["id"],
            "item_id": str(db_item.id),
            "item_title": db_item.title
        })
        return db_item
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}", extra={
            "user_id": current_user["id"],
            "item_title": item.title
        })
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[Item])
async def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str = Query(None, min_length=1)
):
    try:
        if search:
            items = await search_items(search, skip, limit)
        else:
            items = await get_items(skip, limit)
        logger.info(f"Items retrieved: {len(items)}", extra={
            "skip": skip,
            "limit": limit,
            "search": search
        })
        return items
    except Exception as e:
        logger.error(f"Error retrieving items: {str(e)}", extra={
            "skip": skip,
            "limit": limit,
            "search": search
        })
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: str):
    try:
        item = await get_item(item_id)
        if item is None:
            logger.warning(f"Item not found: {item_id}")
            raise HTTPException(status_code=404, detail="Item not found")
        logger.info(f"Item retrieved: {item_id}")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving item: {str(e)}", extra={"item_id": item_id})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{item_id}", response_model=Item)
async def update_existing_item(item_id: str, item: ItemCreate, current_user: dict = Depends(get_current_user)):
    try:
        updated_item = await update_item(item_id, item, current_user["id"])
        if updated_item is None:
            logger.warning(f"Item not found or user not authorized: {item_id}")
            raise HTTPException(status_code=404, detail="Item not found or user not authorized")
        process_item_async.delay(str(updated_item.id))
        logger.info(f"Item updated: {item_id}", extra={
            "user_id": current_user["id"],
            "item_id": item_id
        })
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating item: {str(e)}", extra={
            "user_id": current_user["id"],
            "item_id": item_id
        })
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{item_id}", status_code=204)
async def delete_existing_item(item_id: str, current_user: dict = Depends(get_current_user)):
    try:
        deleted = await delete_item(item_id, current_user["id"])
        if not deleted:
            logger.warning(f"Item not found or user not authorized: {item_id}")
            raise HTTPException(status_code=404, detail="Item not found or user not authorized")
        logger.info(f"Item deleted: {item_id}", extra={
            "user_id": current_user["id"],
            "item_id": item_id
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}", extra={
            "user_id": current_user["id"],
            "item_id": item_id
        })
        raise HTTPException(status_code=500, detail="Internal server error")