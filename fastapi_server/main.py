from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn

from crud import create_task, delete_task, find_all_tasks
from database import engine, get_db
from models import Base
from schemas import TaskDTO

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/tasks")


@app.get("")
def find_all(db: Session = Depends(get_db)):
    return find_all_tasks(db)


@app.post("")
def create(task: TaskDTO, db: Session = Depends(get_db)):
    create_task(db, task)


@app.delete("")
def delete(task: TaskDTO, db: Session = Depends(get_db)):
    delete_task(db, task.id)


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000)
