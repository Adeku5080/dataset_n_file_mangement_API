from pydantic import BaseModel
from typing import List, Dict, Any

from sqlalchemy import JSON

class DatasetCreate(BaseModel):
    title : str
    tags : List[str]
    dataset_metadata: Dict[str, Any]


class DatasetRead(BaseModel):
    title:str
    tags : List[str] 
    user_id :int
    dataset_metadata: Dict[str, Any]


class Config:
        orm_mode = True
