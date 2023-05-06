from fastapi import APIRouter, status, HTTPException, Response
from db.db_inc import engine, Base
from modeles.planning import Planning
from sqlalchemy.orm import sessionmaker

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/plannings")
def read_plannings():
    db = SessionLocal()
    plannings = db.query(Planning).all()
    if plannings is None:
        raise HTTPException(status_code=204, detail="Plannings not found")
    return plannings


@router.get("/plannings/{planning_id}")
def read_planning(planning_id: int):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=204, detail="Planning not found")
    return planning
