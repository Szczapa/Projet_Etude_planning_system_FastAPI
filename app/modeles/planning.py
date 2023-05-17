from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db.db_inc import Base
from datetime import datetime
from pydantic import BaseModel


class Planning(Base):
    __tablename__ = "plannings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    company_id = Column(Integer, index=True)
    creator = Column(Integer, index=True)


class PlanningCreate(BaseModel):
    name: str
    creator: int
    company_id: int


class PlanningParticipant(Base):
    __tablename__ = "planning_participant"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    planning_id = Column(Integer, ForeignKey("plannings.id"), nullable=False)

    class Config:
        orm_mode = True
        exclude = ('user_id',)


class userLeavePlanning(BaseModel):
    user_id: int
    company_id: int