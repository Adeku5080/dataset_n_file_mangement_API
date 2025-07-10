from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)   
    password = Column(String)
    fullname = Column(String)

    datasets = relationship("Dataset", back_populates="user")




