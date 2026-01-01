from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: Optional[int] = None