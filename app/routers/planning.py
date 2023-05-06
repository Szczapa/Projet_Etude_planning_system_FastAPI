from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.planning import Planning, PlanningCreate
from modeles.user import User
from sqlalchemy.orm import sessionmaker
from routers.login import get_current_user
from datetime import datetime, timedelta
from modeles.role import Role

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/plannings")
def read_plannings(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    plannings = db.query(Planning).filter(Planning.company_id == current_user.company_id).all()
    if len(plannings) == 0:
        raise HTTPException(status_code=204, detail="Plannings not found")
    return plannings


@router.get("/plannings/{planning_id}")
def read_planning(planning_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=204, detail="Planning not found")
    if planning.company_id != current_user.company_id:
        raise HTTPException(status_code=204, detail="Planning not found")
    return planning


@router.delete("/plannings/{planning_id}")
def delete_planning(planning_id: int, current_user: User = Depends(get_current_user), Role=Role):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.creator != current_user.id:
        raise HTTPException(status_code=401, detail="Not authorized to delete this planning")
    db.delete(planning)
    db.commit()
    return {"message": "Planning deleted successfully"}


@router.post("/plannings")
def create_planning(planning: PlanningCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    if current_user.role_id != 2:
        raise HTTPException(status_code=401, detail="Not authorized to create plannings")
    else:
        new_planning = Planning(
            name=planning.name,
            creator=current_user.id,
            company_id=current_user.company_id,
            start_date=datetime.today().date(),
            end_date=planning.end_date,
        )
        db.add(new_planning)
        db.commit()
        db.refresh(new_planning)
        return new_planning
