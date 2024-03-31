from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime , Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.Database import Base

class ItemModel(Base) :
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=str(datetime.now()))
    updated_at = Column(DateTime, server_default=str(datetime.now()), onupdate=str(datetime.now()))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="items")
