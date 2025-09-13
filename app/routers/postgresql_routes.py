from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.models.postgresql_models import UserPostgreSQL, UserPostgreSQLSchema, UserPostgreSQLCreate, UserPostgreSQLUpdate
from app.database.postgresql import get_postgresql_session
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/postgresql", tags=["PostgreSQL"])


@router.post("/users/", response_model=UserPostgreSQLSchema)
async def create_user(user: UserPostgreSQLCreate, db: AsyncSession = Depends(get_postgresql_session)):
    """Create a new user in PostgreSQL"""
    try:
        db_user = UserPostgreSQL(**user.dict())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return UserPostgreSQLSchema.model_validate(db_user)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating user in PostgreSQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/users/", response_model=List[UserPostgreSQLSchema])
async def get_users(db: AsyncSession = Depends(get_postgresql_session)):
    """Get all users from PostgreSQL"""
    try:
        result = await db.execute(select(UserPostgreSQL))
        users = result.scalars().all()
        return [UserPostgreSQLSchema.model_validate(user) for user in users]
    except Exception as e:
        logger.error(f"Error retrieving users from PostgreSQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.get("/users/{user_id}", response_model=UserPostgreSQLSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_postgresql_session)):
    """Get a specific user from PostgreSQL"""
    try:
        result = await db.execute(select(UserPostgreSQL).where(UserPostgreSQL.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserPostgreSQLSchema.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user from PostgreSQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.put("/users/{user_id}", response_model=UserPostgreSQLSchema)
async def update_user(user_id: int, user_update: UserPostgreSQLUpdate, db: AsyncSession = Depends(get_postgresql_session)):
    """Update a user in PostgreSQL"""
    try:
        result = await db.execute(select(UserPostgreSQL).where(UserPostgreSQL.id == user_id))
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
        return UserPostgreSQLSchema.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating user in PostgreSQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_postgresql_session)):
    """Delete a user from PostgreSQL"""
    try:
        result = await db.execute(select(UserPostgreSQL).where(UserPostgreSQL.id == user_id))
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
        logger.error(f"Error deleting user from PostgreSQL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )