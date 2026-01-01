from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Database Model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)  # Added name field
    email: str = Field(unique=True, max_length=255)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = Field(default=None)

    # Relationship to todos
    todos: List["Todo"] = Relationship(back_populates="user")


# Database Model
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")  # Required field for authenticated users

    # Relationship to user
    user: Optional[User] = Relationship(back_populates="todos")


# Pydantic Schemas for API
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str  # Added name field
    password: str


class UserRead(UserBase):
    id: int
    name: str  # Added name field
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int  # Required for authenticated todos

    model_config = {"from_attributes": True}


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoComplete(BaseModel):
    completed: bool