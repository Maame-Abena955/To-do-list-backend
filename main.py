from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List as ListType
import models, crud, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5174",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do List API!"}


# ✅ TASK endpoints
@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, list_id: int, db: Session = Depends(get_db)):
    return crud.create_task(db, task, list_id)


@app.get("/tasks", response_model=ListType[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)
):
    db_task = crud.update_task(db, task_id, task_update.title, task_update.completed)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}


@app.patch("/tasks/{task_id}/completed")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.mark_completed(db, task_id, True)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.patch("/tasks/{task_id}/uncompleted")
def uncomplete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.mark_completed(db, task_id, False)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)


# ✅ LIST endpoints
@app.post("/lists", response_model=schemas.List)
def create_list(list_data: schemas.ListCreate, db: Session = Depends(get_db)):
    return crud.create_list(db, list_data)


@app.get("/lists", response_model=ListType[schemas.List])
def read_lists(db: Session = Depends(get_db)):
    return crud.get_lists(db)


@app.get("/lists/{list_id}", response_model=schemas.List)
def read_list(list_id: int, db: Session = Depends(get_db)):
    db_list = crud.get_list(db, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    return db_list


@app.delete("/lists/{list_id}")
def delete_list(list_id: int, db: Session = Depends(get_db)):
    success = crud.delete_list(db, list_id)
    if not success:
        raise HTTPException(status_code=404, detail="List not found")
    return {"detail": "List deleted"}


@app.get("/lists/{list_id}/tasks", response_model=ListType[schemas.Task])
def get_tasks_by_list(list_id: int, db: Session = Depends(get_db)):
    tasks = crud.get_tasks_by_list(db, list_id)
    if tasks is None:
        raise HTTPException(status_code=404, detail="List not found or has no tasks")
    return tasks




