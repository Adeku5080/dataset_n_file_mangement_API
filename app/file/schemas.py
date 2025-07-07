from pydantic import BaseModel

class FileCreate(BaseModel):
    filename= str
    dataset_id = int 

class FileRead(BaseModel):
    id: int
    filename: str
    file_type: str  
    size: int       
    extension: str 
    storage_url: str
    uploaded_by: int
    uploaded_at: datetime
    dataset_id: int | None    