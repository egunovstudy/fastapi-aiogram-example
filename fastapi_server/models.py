from sqlalchemy import Column, Integer, String

from database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True, nullable=False)
    date = Column(String, unique=True, index=True, nullable=False)
