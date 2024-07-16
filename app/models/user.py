from sqlalchemy import Column, Integer, String
from utils.db import Base
from pydantic import BaseModel, EmailStr, SecretStr


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr
