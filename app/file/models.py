from app.database import Base
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String,ForeignKey,DateTime



class File(Base):
    __tablename__ = "files"

    id = Column(Integer,primary_key=True ,index=True) 
    filename=Column(String)
    file_type=Column(String,index=True)
    storage_url=Column(String)
    size =Column(Integer)
    extension = Column(String)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    uploaded_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    

