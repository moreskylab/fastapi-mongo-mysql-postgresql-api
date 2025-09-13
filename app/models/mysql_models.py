from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.mysql import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserMySQL(Base):
    """MySQL User table"""
    __tablename__ = "users_mysql"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class UserMySQLSchema(BaseModel):
    """Pydantic schema for MySQL User"""
    model_config = ConfigDict(from_attributes=True)
    
    id: Optional[int] = None
    name: str
    email: str
    age: int
    created_at: Optional[datetime] = None


class UserMySQLCreate(BaseModel):
    """Create user schema for MySQL"""
    name: str
    email: str
    age: int


class UserMySQLUpdate(BaseModel):
    """Update user schema for MySQL"""
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None