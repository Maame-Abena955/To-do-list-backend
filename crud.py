from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    return db.query(Task).all()


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate):
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, title: str, description: str):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    if title:
        db_task.title = title
    if description:
        db_task.description = description
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


def mark_completed(db: Session, task_id: int, status: bool):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    db_task.completed = status
    db.commit()
    db.refresh(db_task)
    return db_task


def get_stats(db: Session):
    total = db.query(Task).count()
    completed = db.query(Task).filter(Task.completed == True).count()
    pending = total - completed
    return {"total": total, "completed": completed, "pending": pending}

