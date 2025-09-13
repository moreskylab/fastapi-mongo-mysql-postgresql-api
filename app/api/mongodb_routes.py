from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
from datetime import datetime
from app.models.schemas import UserCreate, UserUpdate, UserResponse, HealthCheck
from app.db.mongodb import get_mongo_database

router = APIRouter(prefix="/mongodb", tags=["MongoDB"])


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check for MongoDB"""
    try:
        db = get_mongo_database()
        await db.command("ping")
        return HealthCheck(
            status="healthy",
            database="MongoDB",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB health check failed: {str(e)}"
        )


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user in MongoDB"""
    try:
        db = get_mongo_database()
        user_data = user.model_dump()
        user_data["id"] = str(uuid.uuid4())
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = None
        
        result = await db.users.insert_one(user_data)
        if result.inserted_id:
            return UserResponse(**user_data)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/users", response_model=List[UserResponse])
async def get_users():
    """Get all users from MongoDB"""
    try:
        db = get_mongo_database()
        users = []
        async for user in db.users.find():
            user.pop("_id", None)  # Remove MongoDB _id field
            users.append(UserResponse(**user))
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a specific user by ID from MongoDB"""
    try:
        db = get_mongo_database()
        user = await db.users.find_one({"id": user_id})
        if user:
            user.pop("_id", None)  # Remove MongoDB _id field
            return UserResponse(**user)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    """Update a user in MongoDB"""
    try:
        db = get_mongo_database()
        update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided for update"
            )
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db.users.update_one(
            {"id": user_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        updated_user = await db.users.find_one({"id": user_id})
        updated_user.pop("_id", None)  # Remove MongoDB _id field
        return UserResponse(**updated_user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete a user from MongoDB"""
    try:
        db = get_mongo_database()
        result = await db.users.delete_one({"id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )