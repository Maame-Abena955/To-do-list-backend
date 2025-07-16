from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 👈 Add this
from sqlalchemy.orm import Session
from typing import List
import models
import crud
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Add this CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do List API!"}


@app.get("/tasks", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)
):
    db_task = crud.update_task(db, task_id, task_update.title, task_update.description)
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
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.completed:
        raise HTTPException(status_code=400, detail="Task is already completed")
    return crud.mark_completed(db, task_id, True)


@app.patch("/tasks/{task_id}/uncompleted")
def uncomplete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not db_task.completed:
        raise HTTPException(status_code=400, detail="Task is already uncompleted")
    return crud.mark_completed(db, task_id, False)


@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)

