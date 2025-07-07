from pydantic import BaseModel
from typing import List

class DatasetCreate(BaseModel):
    title : str
    tags : List[str]


class DatasetRead(BaseModel):
    title:str
    tags : List[str] 
    user_id :int

class Config:
        orm_mode = True
