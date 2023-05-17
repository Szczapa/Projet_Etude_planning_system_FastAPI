from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time, Date
from db.db_inc import Base
from datetime import datetime, date, time
from pydantic import BaseModel


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    planning_id = Column(Integer, index=True)
    name = Column(String(255), unique=True, index=True)
    date = Column(Date, index=True)
    place = Column(String(255), index=True)
    creator_id = Column(Integer, index=True)
    company_id = Column(Integer, index=True)
    start_time = Column(Time, index=True)
    end_time = Column(Time, index=True)


class ActivityCreate(BaseModel):
    planning_id: int
    name: str
    date: date
    place: str
    creator_id: int
    company_id: int
    start_time: time
    end_time: time

class ActivityParticipants(Base):
    __tablename__ = "activity_participants"
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)

class userJoinActivity(BaseModel):
    user_id: int