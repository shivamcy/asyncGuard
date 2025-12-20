from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from app.config.db import Base

class User(Base):
    __tablename__= "users"
    
    id=Column(Integer, primary_key=True,unique=True)
    email=Column(String(255),unique=True,index=True,nullable=False)
    hashed_password=Column(String , nullable=False)
    role=Column(String(50), nullable=False)
    org_id=Column(Integer,ForeignKey("organizations.id"),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
