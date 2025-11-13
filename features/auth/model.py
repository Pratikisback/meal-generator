from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True) 
    password = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False) 
    is_verified = Column(Boolean, default=False) 
    
