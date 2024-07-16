from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from utils.db import Base
from pydantic import BaseModel, constr

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="posts")

class PostCreate(BaseModel):
    text: constr(max_length=1_000_000)
