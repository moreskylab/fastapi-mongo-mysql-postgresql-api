from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.models.mysql_models import UserMySQL, UserMySQLSchema, UserMySQLCreate, UserMySQLUpdate
from app.database.mysql import get_mysql_session
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mysql", tags=["MySQL"])


@router.post("/users/", response_model=UserMySQLSchema)
async def create_user(user: UserMySQLCreate, db: AsyncSession = Depends(get_mysql_session)):
    """Create a new user in MySQL"""
    try:
        db_user = UserMySQL(**user.dict())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return UserMySQLSchema.model_validate(db_user)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating user in MySQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/users/", response_model=List[UserMySQLSchema])
async def get_users(db: AsyncSession = Depends(get_mysql_session)):
    """Get all users from MySQL"""
    try:
        result = await db.execute(select(UserMySQL))
        users = result.scalars().all()
        return [UserMySQLSchema.model_validate(user) for user in users]
    except Exception as e:
        logger.error(f"Error retrieving users from MySQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get("/users/{user_id}", response_model=UserMySQLSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_mysql_session)):
    """Get a specific user from MySQL"""
    try:
        result = await db.execute(select(UserMySQL).where(UserMySQL.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserMySQLSchema.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user from MySQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.put("/users/{user_id}", response_model=UserMySQLSchema)
async def update_user(user_id: int, user_update: UserMySQLUpdate, db: AsyncSession = Depends(get_mysql_session)):
    """Update a user in MySQL"""
    try:
        result = await db.execute(select(UserMySQL).where(UserMySQL.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        return UserMySQLSchema.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating user in MySQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_mysql_session)):
    """Delete a user from MySQL"""
    try:
        result = await db.execute(select(UserMySQL).where(UserMySQL.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        await db.delete(user)
        await db.commit()
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting user from MySQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )