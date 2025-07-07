from sqlalchemy import Column, Integer, String,ForeignKey
from app.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer,primary_key=true ,index=True) 
    filename=Column(String)
    file_type=Column(String,index=True)
    storage_url=Column(String)
    size =Column(Integer)
    extension = Column(String)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)   

    

