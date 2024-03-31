from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime 
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.Database import Base

class UserModel(Base) :
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=str(datetime.now()))
    updated_at = Column(DateTime, server_default=str(datetime.now()), onupdate=str(datetime.now()))

    items = relationship("ItemModel", back_populates="user")