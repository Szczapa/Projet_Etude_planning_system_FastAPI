from db.db_inc import engine, SessionLocal, Base
from sqlalchemy import Column, Integer, String


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50), unique=True, index=True)
