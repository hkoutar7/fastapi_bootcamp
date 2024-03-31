from pydantic import BaseModel, BaseConfig
import datetime


class UserBaseSchema(BaseModel) :
    first_name : str
    last_name : str
    
    class Config(BaseConfig):
        from_attributes = True
        orm_mode = True
        arbitrary_types_allowed = True


class UserCreateSchema(UserBaseSchema) :
    email : str
    password : str


class UserUpdateSchema(UserBaseSchema) :
    pass


class UserSchema(UserBaseSchema) :
    id : int
    email : str
    is_active : bool
    created_at : datetime
    updated_at : datetime