from datetime import datetime
from pydantic import BaseModel
from typing import List

class FileCreate(BaseModel):
    filename: str
    dataset_id: int 

class FileRead(BaseModel):
    id: int
    filename: str
    file_type: str  
    size: int       
    extension: str 
    storage_url: str
    uploaded_by: int
    uploaded_at: datetime
    dataset_id: int    


class PartModel(BaseModel):
    PartNumber: int
    ETag: str

class CompleteUploadModel(BaseModel):
    key: str
    upload_id: str
    parts: List[PartModel]
    filename: str
    dataset_id: int
    uploaded_by: int 