from db.db_inc import engine, SessionLocal, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel, Field
from typing import Optional

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(255), index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role_id: int
    company_id: int


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role_id: int
    company_id: int
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Username of the user")
    email: Optional[str] = Field(None, description="Email of the user")
    role_id: Optional[int] = Field(None, description="Role ID of the user")
    password: Optional[str] = Field(None, description="Password of the user")
