from sqlalchemy.orm import Session
from models import Task, List
from schemas import TaskCreate, TaskUpdate, ListCreate


# Tasks
def get_tasks(db: Session):
    return db.query(Task).all()


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate, list_id: int):
    db_task = Task(title=task.title, list_id=list_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, title: str, completed: bool):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    if title is not None:
        db_task.title = title
    if completed is not None:
        db_task.completed = completed
        if completed:
            db_task.completed_at = db_task.updated_at
        else:
            db_task.completed_at = None
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
        return None
    db_task.completed = status
    if status:
        db_task.completed_at = db_task.updated_at
    else:
        db_task.completed_at = None
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_by_list(db: Session, list_id: int):
    return db.query(Task).filter(Task.list_id == list_id).all()


def get_stats(db: Session):
    total = db.query(Task).count()
    completed = db.query(Task).filter(Task.completed == True).count()
    pending = total - completed
    return {"total": total, "completed": completed, "pending": pending}


# Lists
def create_list(db: Session, list_data: ListCreate):
    db_list = List(name=list_data.name, description=list_data.description)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    for task in list_data.tasks:
        create_task(db, task, db_list.id)
    db.refresh(db_list)
    return db_list


def get_list(db: Session, list_id: int):
    return db.query(List).filter(List.id == list_id).first()


def get_lists(db: Session):
    return db.query(List).all()


def delete_list(db: Session, list_id: int):
    db_list = db.query(List).filter(List.id == list_id).first()
    if not db_list:
        return False
    db.delete(db_list)
    db.commit()
    return True


