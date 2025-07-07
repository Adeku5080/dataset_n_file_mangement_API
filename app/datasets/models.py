from sqlalchemy import Column, Integer, String,ForeignKey,Text, UniqueConstraint
from app.database import Base
from sqlalchemy.dialects.postgresql import ARRAY 
from sqlalchemy.orm import relationship

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer,primary_key=True,index=True)
    title =Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(ARRAY(Text))
