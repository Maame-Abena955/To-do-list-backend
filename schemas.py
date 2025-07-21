from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List as ListType


class TaskBase(BaseModel):
    title: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    id: int
    completed: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]
    list_id: int

    class Config:
        orm_mode = True


class ListBase(BaseModel):
    name: str
    description: Optional[str] = None


class ListCreate(ListBase):
    tasks: Optional[ListType[TaskCreate]] = []


class List(ListBase):
    id: int
    tasks: ListType[Task] = []

    class Config:
        orm_mode = True

