from sqlalchemy import Column, Boolean, Integer, String, DateTime
from sqlalchemy import func

from database.database import Base

class UserModel(Base) :
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
