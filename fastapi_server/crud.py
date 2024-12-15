from sqlalchemy.orm import Session

from models import Task
from schemas import TaskDTO


def find_all_tasks(db: Session):
    return db.query(Task).all()


def create_task(db: Session, task_dto: TaskDTO):
    db_task = Task(text=task_dto.text, date=task_dto.date)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db.query(Task).filter(Task.id == task_id).delete()
    db.commit()
