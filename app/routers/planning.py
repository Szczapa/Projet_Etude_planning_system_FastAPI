from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.planning import Planning, PlanningCreate, PlanningParticipant, userLeavePlanning, userJoinPlanning
from modeles.user import User
from sqlalchemy.orm import sessionmaker
from routers.login import get_current_user
from pydantic import BaseModel
from utils.admin import is_admin, is_maintainer

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/plannings")
def read_plannings(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    if is_maintainer(current_user):
        plannings = db.query(Planning).all()
    else:
        plannings = db.query(Planning).filter(Planning.company_id == current_user.company_id).all()
    if len(plannings) == 0:
        raise HTTPException(status_code=404, detail="Plannings not found")
    return plannings


@router.get("/plannings/{planning_id}")
def read_planning(planning_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if not is_maintainer(current_user):
        if planning.company_id != current_user.company_id:
            raise HTTPException(status_code=404, detail="Planning not found")
    return planning


@router.get("/planning/{planning_id}/participants")
def read_planning_participants(planning_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.company_id != current_user.company_id and not is_maintainer(current_user):
        raise HTTPException(status_code=401, detail="Not a company planning")
    else:
        planning = db.query(Planning).filter(Planning.id == planning_id).first()
        if planning is None:
            raise HTTPException(status_code=404, detail="Planning not found")
        participants = db.query(PlanningParticipant).filter_by(planning_id=planning_id).all()
        if len(participants) == 0:
            raise HTTPException(status_code=404, detail="No participants to this planning")
        elif is_admin(current_user):
            participant_ids = [participant.user_id for participant in participants]
            return {"Id des participants": participant_ids}
        else:
            return {"number_of_participants": len(participants)}


@router.post("/planning")
def create_planning(planning: PlanningCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    if not is_admin(current_user):
        raise HTTPException(status_code=401, detail="Not authorized to create plannings")

    if is_maintainer(current_user):
        if planning.creator != current_user.id:
            raise HTTPException(status_code=401, detail="Not authorized to create plannings for this user")
        new_planning = Planning(
            name=planning.name,
            creator=current_user.id,
            company_id=planning.company_id
        )
    else:
        if planning.company_id != current_user.company_id:
            raise HTTPException(status_code=401, detail="Not authorized to create plannings for this company")
        if planning.creator != current_user.id:
            raise HTTPException(status_code=401, detail="Not authorized to create plannings for this user")
        new_planning = Planning(
            name=planning.name,
            creator=current_user.id,
            company_id=current_user.company_id
        )

    db.add(new_planning)
    db.commit()
    db.refresh(new_planning)
    return new_planning


@router.post("/planning/{planning_id}/join")
def join_planning(
        planning_id: int,
        userJoin: userJoinPlanning,
        current_user: User = Depends(get_current_user)
):
    # check if user to add is same as connected user or if connected user if maintainer else, raise 403
    if current_user.id != userJoin.user_id and not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to add this user")
    db = SessionLocal()
    user = db.query(User).filter(User.id == userJoin.user_id).one()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.company_id != user.company_id:
        raise HTTPException(status_code=401, detail="Not planning corresponding to this company")
    else:
        participant = db.query(PlanningParticipant).filter_by(
            user_id=user.id,
            planning_id=planning_id
        ).first()
        if participant is not None:
            raise HTTPException(status_code=409, detail="User already joined this planning")
        new_participant = PlanningParticipant(
            planning_id=planning_id,
            user_id=user.id
        )
        db.add(new_participant)
        db.commit()
        db.refresh(new_participant)
        return new_participant


@router.delete("/planning/{planning_id}")
def delete_planning(planning_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")

    if planning.creator != current_user.id or not is_admin(current_user):
        raise HTTPException(status_code=401, detail="Not authorized to delete this planning")
    if is_admin(current_user) and not is_maintainer(current_user):
        if planning.company_id != current_user.company_id:
            raise HTTPException(status_code=401, detail="Not authorized to delete this planning")
    db.delete(planning)
    db.commit()
    return {"message": "Planning deleted successfully"}


@router.delete("/planning/{planning_id}/leave/{user_id}")
def leave_planning(
        planning_id: int,
        user_id: int,
        current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.company_id != current_user.company_id and not is_maintainer(current_user):
        raise HTTPException(status_code=401, detail="Not authorized to interact with this planning")
    else:
        participant = db.query(PlanningParticipant).filter_by(
            user_id=user_id,
            planning_id=planning_id
        ).first()
        if participant.user_id != current_user.id or not is_admin(current_user):
            raise HTTPException(status_code=401, detail="Not authorized to delete this user")
        if participant is None:
            raise HTTPException(status_code=409, detail="User already left this planning")
        db.delete(participant)
        db.commit()
        return {"message": "User successfully left planning"}
