from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.mongo_models import UserMongo, UserMongoCreate, UserMongoUpdate
from app.database.mongodb import get_database
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mongodb", tags=["MongoDB"])


@router.post("/users/", response_model=UserMongo)
async def create_user(user: UserMongoCreate):
    """Create a new user in MongoDB"""
    try:
        database = await get_database()
        if not database:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB is not available"
            )
        
        user_dict = user.dict()
        user_dict["created_at"] = datetime.utcnow()
        
        result = await database.users.insert_one(user_dict)
        
        # Get the created user
        created_user = await database.users.find_one({"_id": result.inserted_id})
        created_user["_id"] = str(created_user["_id"])
        
        return UserMongo(**created_user)
    except Exception as e:
        logger.error(f"Error creating user in MongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/users/", response_model=List[UserMongo])
async def get_users():
    """Get all users from MongoDB"""
    try:
        database = await get_database()
        if not database:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB is not available"
            )
        
        users = []
        async for user in database.users.find():
            user["_id"] = str(user["_id"])
            users.append(UserMongo(**user))
        
        return users
    except Exception as e:
        logger.error(f"Error retrieving users from MongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get("/users/{user_id}", response_model=UserMongo)
async def get_user(user_id: str):
    """Get a specific user from MongoDB"""
    try:
        database = await get_database()
        if not database:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB is not available"
            )
        
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        user = await database.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user["_id"] = str(user["_id"])
        return UserMongo(**user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user from MongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.put("/users/{user_id}", response_model=UserMongo)
async def update_user(user_id: str, user_update: UserMongoUpdate):
    """Update a user in MongoDB"""
    try:
        database = await get_database()
        if not database:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB is not available"
            )
        
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        result = await database.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get updated user
        updated_user = await database.users.find_one({"_id": ObjectId(user_id)})
        updated_user["_id"] = str(updated_user["_id"])
        
        return UserMongo(**updated_user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user in MongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete a user from MongoDB"""
    try:
        database = await get_database()
        if not database:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="MongoDB is not available"
            )
        
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )
        
        result = await database.users.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user from MongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )