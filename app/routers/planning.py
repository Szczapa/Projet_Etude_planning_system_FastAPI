from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.planning import Planning, PlanningCreate, PlanningParticipant
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
        raise HTTPException(status_code=404, detail="Plannings not found")
    return plannings


# @router.get("/plannings/{planning_id}")
# def read_planning(planning_id: int, current_user: User = Depends(get_current_user)):
#     db = SessionLocal()
#     planning = db.query(Planning).filter(Planning.id == planning_id).first()
#     if planning is None:
#         raise HTTPException(status_code=404, detail="Planning not found")
#     if planning.company_id != current_user.company_id:
#         raise HTTPException(status_code=404, detail="Planning not found")
#     return planning


@router.delete("/plannings/{planning_id}")
def delete_planning(planning_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.creator != current_user.id or current_user.role_id != 2:
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
            company_id=current_user.company_id
        )
        db.add(new_planning)
        db.commit()
        db.refresh(new_planning)
        return new_planning


@router.post("/planning/{planning_id}/join")
def join_planning(
        planning_id: int,
        current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.company_id != current_user.company_id:
        raise HTTPException(status_code=401, detail="Not authorized to interact with this planning")
    else:
        participant = db.query(PlanningParticipant).filter_by(
            user_id=current_user.id,
            planning_id=planning_id
        ).first()
        if participant is not None:
            raise HTTPException(status_code=409, detail="User already joined this planning")
        new_participant = PlanningParticipant(
            planning_id=planning_id,
            user_id=current_user.id
        )
        db.add(new_participant)
        db.commit()
        db.refresh(new_participant)
        return new_participant


@router.delete("/planning/leave/{planning_id}")
def leave_planning(
        planning_id: int,
        current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.company_id != current_user.company_id:
        raise HTTPException(status_code=401, detail="Not authorized to interact with this planning")
    else:
        participant = db.query(PlanningParticipant).filter_by(
            user_id=current_user.id,
            planning_id=planning_id
        ).first()
        if participant is None:
            raise HTTPException(status_code=409, detail="User already left this planning")
        db.delete(participant)
        db.commit()
        return {"message": "User successfully left planning"}


@router.get("/planning/{planning_id}/participants")
def read_planning_participants(planning_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.company_id != current_user.company_id:
        raise HTTPException(status_code=401, detail="Not authorized to interact with this planning")
    else:
        participants = db.query(PlanningParticipant).filter_by(planning_id=planning_id).all()
        if len(participants) == 0:
            raise HTTPException(status_code=404, detail="Participants not found")
        elif current_user.role_id == 2:
            participant_ids = [participant.user_id for participant in participants]
            return {"Id des participants": participant_ids}
        else:
            return {"number_of_participants": len(participants)}


@router.post('/planning_add_user/{planning_id}/{user_id}')
def add_user_to_planning(planning_id: int, user_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    if current_user.role_id != 2:
        raise HTTPException(status_code=401, detail="Not authorized to add users to plannings")
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.company_id != current_user.company_id:
        raise HTTPException(status_code=401, detail="Not authorized to interact with this planning")

    user = db.query(User).filter(User.id == user_id, current_user.company_id == User.company_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        participant = db.query(PlanningParticipant).filter_by(
            user_id=user_id,
            planning_id=planning_id
        ).first()
        if participant is not None:
            raise HTTPException(status_code=409, detail="User already joined this planning")
        new_participant = PlanningParticipant(
            planning_id=planning_id,
            user_id=user_id
        )
        db.add(new_participant)
        db.commit()
        db.refresh(new_participant)
        return new_participant

@router.delete('/planning_delete_user/{planning_id}/{user_id}')
def delete_user_from_planning(planning_id: int, user_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    if current_user.role_id != 2:
        raise HTTPException(status_code=401, detail="Not authorized to remove users from plannings")
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if planning is None:
        raise HTTPException(status_code=404, detail="Planning not found")
    if planning.company_id != current_user.company_id:
        raise HTTPException(status_code=401, detail="Not authorized to interact with this planning")

    user = db.query(User).filter(User.id == user_id, current_user.company_id == User.company_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        participant = db.query(PlanningParticipant).filter_by(
            user_id=user_id,
            planning_id=planning_id
        ).first()
        if participant is None:
            raise HTTPException(status_code=404, detail="User is not part of this planning")
        db.delete(participant)
        db.commit()
        return {"message": "User successfully removed from the planning"}

