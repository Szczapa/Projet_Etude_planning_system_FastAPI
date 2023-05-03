from db.db_inc import engine, SessionLocal, Base
from sqlalchemy import Column, Integer, String


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
