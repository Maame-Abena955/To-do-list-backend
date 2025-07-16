from pydantic import BaseModel
from typing import Optional, List


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True


class ListBase(BaseModel):
    name: str


class ListCreate(ListBase):
    pass


class List(ListBase):
    id: int
    tasks: List[Task] = []

    class Config:
        orm_mode = True
