from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON , DateTime
from sqlalchemy.sql import func
from app.config.db import Base

class AuditResult(Base):
    __tablename__ = "audit_results"

    id = Column(Integer, primary_key=True)
    audit_run_id = Column(Integer, ForeignKey("audit_runs.id"), nullable=False)
    check_name = Column(String(255), nullable=False)
    passed = Column(Boolean, nullable=False)
    severity = Column(String(50), nullable=False)
    details = Column(JSON, nullable=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    
