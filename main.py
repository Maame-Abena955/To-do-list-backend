from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Welcome to the To-Do List API!"}


@app.post("/lists", response_model=schemas.List)
def create_list(name: str, db: Session = Depends(get_db)):
    return crud.create_list(db, name)


@app.get("/lists", response_model=List[schemas.List])
def get_lists(db: Session = Depends(get_db)):
    return crud.get_lists(db)


@app.delete("/lists/{list_id}")
def delete_list(list_id: int, db: Session = Depends(get_db)):
    success = crud.delete_list(db, list_id)
    if not success:
        raise HTTPException(status_code=404, detail="List not found")
    return {"detail": "List deleted"}


@app.post("/lists/{list_id}/tasks", response_model=schemas.Task)
def create_task_in_list(
    list_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    return crud.create_task_in_list(db, list_id, task)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task.title, task.description)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}


@app.patch("/tasks/{task_id}/completed", response_model=schemas.Task)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.mark_completed(db, task_id, True)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.patch("/tasks/{task_id}/uncompleted", response_model=schemas.Task)
def uncomplete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.mark_completed(db, task_id, False)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)

