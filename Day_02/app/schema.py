from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreateProductSchema(BaseModel) :
    title : str
    content : Optional[str]


class ProductSchema (CreateProductSchema) :
    id : int
    is_published : Optional[bool] = False
    created_at : Optional[datetime] = datetime.now


class UpdateProductSchema (CreateProductSchema) :
    is_published : Optional[bool] = False