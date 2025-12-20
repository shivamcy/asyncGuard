from sqlalchemy import  Column, Integer, ForeignKey, DateTime, UniqueConstraint 
from sqlalchemy.sql import func
from app.config.db import Base

class AuditRun(Base):
    __tablename__="audit_runs"
    
    id=Column(Integer , nullable=False , primary_key=True)
    api_id=Column(Integer, ForeignKey("api_endpoints.id"),nullable=False)
    score=Column(Integer, nullable=False)
    time_window=Column(DateTime(timezone=True), nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
    __table_args__=(
        UniqueConstraint("api_id", "time_window", name="uq_api_timewindow"),
    )
    