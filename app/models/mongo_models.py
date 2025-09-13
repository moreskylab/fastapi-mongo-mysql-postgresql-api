from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserMongo(BaseModel):
    """MongoDB User model"""
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: str
    age: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserMongoCreate(BaseModel):
    """Create user model for MongoDB"""
    name: str
    email: str
    age: int


class UserMongoUpdate(BaseModel):
    """Update user model for MongoDB"""
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None