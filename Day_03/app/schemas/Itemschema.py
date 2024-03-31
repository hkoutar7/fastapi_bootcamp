from typing import Optional
from pydantic import BaseModel, BaseConfig
import datetime


class ItemBaseSchema(BaseModel) :
    name : str
    description : Optional[str] = ""

    class Config(BaseConfig):
        from_attributes = True
        orm_mode = True
        arbitrary_types_allowed = True


class ItemCreateSchema(ItemBaseSchema) :
    pass

class ItemSchema(ItemBaseSchema) :
    id : int
    created_at : datetime
    updated_at : datetime
    user_id : int
    