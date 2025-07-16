import models, schemas
from sqlalchemy.orm import Session


def create_list(db: Session, name: str):
    db_list = models.List(name=name)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


def get_lists(db: Session):
    return db.query(models.List).all()


def get_list(db: Session, list_id: int):
    return db.query(models.List).filter(models.List.id == list_id).first()


def delete_list(db: Session, list_id: int):
    db_list = get_list(db, list_id)
    if not db_list:
        return False
    db.delete(db_list)
    db.commit()
    return True


def create_task_in_list(db: Session, list_id: int, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict(), list_id=list_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, title: str, description: str):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db_task.title = title
    db_task.description = description
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


def mark_completed(db: Session, task_id: int, completed: bool):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db_task.completed = completed
    db.commit()
    db.refresh(db_task)
    return db_task


def get_stats(db: Session):
    total_tasks = db.query(models.Task).count()
    completed_tasks = (
        db.query(models.Task).filter(models.Task.completed == True).count()
    )
    total_lists = db.query(models.List).count()
    return {
        "todoLists": total_lists,
        "totalTasks": total_tasks,
        "completed": completed_tasks,
        "doneToday": 0,  # optional, you can improve this
    }
