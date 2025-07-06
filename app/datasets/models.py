from sqlalchemy import Column, Integer, String
from app.database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer,primary_key+True,index=True)
    title =Column(String)
    user_id = Column(UUID, ForeignKey("users.id"))
    tags = Column(ARRAY(Text))


    __table_args__ = (
    UniqueConstraint("user_id", "title", name="uq_user_dataset_title"),
)
