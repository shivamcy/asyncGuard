from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.config.db import Base

class DeadLetterTask(Base):
    __tablename__ = "dead_letter_tasks"

    id = Column(Integer, primary_key=True)
    task_name = Column(String(255), nullable=False)
    payload = Column(Text, nullable=True)
    error = Column(Text, nullable=False)
    retry_count = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
 