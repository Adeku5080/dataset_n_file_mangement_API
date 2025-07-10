from sqlalchemy import Column, Integer, String,ForeignKey,Text, UniqueConstraint
from app.database import Base
from sqlalchemy.dialects.postgresql import ARRAY ,JSONB
from sqlalchemy.orm import relationship

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer,primary_key=True,index=True)
    title =Column(String,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    tags = Column(ARRAY(Text), default=[])
    dataset_metadata = Column(JSONB, nullable=False) 

    user = relationship("User", back_populates="datasets")  


