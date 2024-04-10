from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBaseSchema(BaseModel) :
    email : EmailStr


class UserCreateSchema(UserBaseSchema) :
    password : str


class UserUpdateSchema(UserBaseSchema) :
    first_name : str
    last_name : str
    is_verified : bool


class UserSchema(UserBaseSchema) :
    id : int
    email : str
    first_name : Optional[str]
    last_name : Optional[str]
    is_verified : bool
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True
        from_attributes = True 

