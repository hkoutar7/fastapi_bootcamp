from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BasePost(BaseModel) :
    title : str
    description : Optional[str]
    published_date : Optional[datetime] = datetime.now()

class CreatePost(BasePost) :
    pass

class Post(BasePost) :
    id : int




