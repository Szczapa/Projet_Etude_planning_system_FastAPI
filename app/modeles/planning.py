from sqlalchemy import Column, Integer, String, DateTime
from db.db_inc import Base
from datetime import datetime
from pydantic import BaseModel

class Planning(Base):
    __tablename__ = "plannings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    company_id = Column(Integer, index=True)
    creator = Column(Integer, index=True)
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)


class PlanningCreate(BaseModel):
    name: str
    creator: int
    company_id: int
    start_date: datetime
    end_date: datetime
