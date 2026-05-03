from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)           # правильный ответ
    difficulty = Column(Float, default=3.0)           # 1..5
    grade = Column(Integer, nullable=False)           # класс (7,8,9,10,11)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    # Связь с темой
    topic = relationship("Topic", back_populates="tasks")

# Добавим связь в модель Topic (обратная ссылка)
# Для этого в файле topic.py нужно добавить:
# from sqlalchemy.orm import relationship
# tasks = relationship("Task", back_populates="topic")