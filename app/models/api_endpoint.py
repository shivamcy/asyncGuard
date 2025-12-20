from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.config.db import Base

class ApiEndpoints(Base):
    __tablename__="api_endpoints"
    id = Column(Integer, primary_key=True , nullable=False)
    name=Column(String(255), )
    url=Column(String(1024), nullable=False)
    is_active = Column(Boolean, default=True)
    org_id=Column(Integer, ForeignKey("organizations.id"),nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
