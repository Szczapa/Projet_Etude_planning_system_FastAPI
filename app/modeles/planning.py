from db.db_inc import engine, SessionLocal, Base
from sqlalchemy import Column, Integer, String

class Planning(Base):
    __tablename__ = "plannings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    company_id = Column(Integer, index=True)
    creator = Column(Integer, index=True)
    start_date = Column(String(50), index=True)
    end_date = Column(String(50), index=True)


