# backend/app/services/mongodb_service.py

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.models.item import Item, ItemCreate
from app.models.user import User, UserCreate

client = AsyncIOMotorClient("mongodb://mongodb:27017")
db = client.lost_and_found

async def get_user_by_email(email: str):
    user = await db.users.find_one({"email": email})
    if user:
        return User(**user)
    return None

async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["password"] = hash_password(user_dict["password"])
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return User(**user_dict)

async def create_item(item: ItemCreate, user_id: str):
    item_dict = item.dict()
    item_dict["user_id"] = user_id
    result = await db.items.insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return Item(**item_dict)

async def get_items(skip: int = 0, limit: int = 100):
    cursor = db.items.find().skip(skip).limit(limit)
    items = await cursor.to_list(length=limit)
    return [Item(**item) for item in items]

async def get_item(item_id: str):
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if item:
        item["id"] = str(item["_id"])
        return Item(**item)
    return None

async def update_item(item_id: str, item: ItemCreate, user_id: str):
    item_dict = item.dict()
    result = await db.items.update_one(
        {"_id": ObjectId(item_id), "user_id": user_id},
        {"$set": item_dict}
    )
    if result.modified_count:
        return await get_item(item_id)
    return None

async def delete_item(item_id: str, user_id: str):
    result = await db.items.delete_one({"_id": ObjectId(item_id), "user_id": user_id})
    return result.deleted_count > 0

def hash_password(password: str):
    # Implement password hashing here
    pass