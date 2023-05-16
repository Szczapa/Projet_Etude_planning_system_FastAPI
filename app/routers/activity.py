from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.activity import Activity, ActivityCreate, ActivityParticipants
from modeles.planning import PlanningParticipant
from sqlalchemy.orm import sessionmaker, Session
from modeles.user import User
from modeles.planning import Planning
from routers.login import get_current_user
from datetime import datetime, timedelta

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/activities")
def read_activities(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    activities = db.query(Activity).filter(User.company_id == Activity.company_id).all()
    if len(activities) == 0:
        raise HTTPException(status_code=404, detail="Activities not found")
    return activities


@router.get("/activity/{activity_id}")
def read_activity(activity_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    activity = db.query(Activity).filter(Activity.id == activity_id,
                                         current_user.company_id == Activity.company_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/create/activity/{planning_id}")
def create_activity(planning_id: int, activity: ActivityCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    if not isCompanyPlanning(planning_id, current_user.company_id, db):
        raise HTTPException(status_code=422, detail="Invalid planning ID")
    if not isInPlanning(planning_id, current_user.id, db):
        raise HTTPException(status_code=422, detail="User not in planning")

    new_activity = Activity(
        name=activity.name,
        planning_id=planning_id,
        creator_id=current_user.id,
        company_id=current_user.company_id,
        date=datetime.today().date(),
        place=activity.place,
        start_time=activity.start_time,
        end_time=activity.end_time,
    )
    db.add(new_activity)
    db.commit()
    return {"message": "Activity created successfully"}


@router.delete("/activity/{activity_id}/delete")
def delete_activity(activity_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    activity = db.query(Activity).filter(Activity.id == activity_id,
                                         current_user.company_id == Activity.company_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    elif activity.creator_id != current_user.id or current_user.role != 2:
        raise HTTPException(status_code=401, detail="Unauthorized")
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


@router.post("/activity/{activity_id}/join")
def join_activity(activity_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    activity = db.query(Activity).filter(Activity.id == activity_id,
                                         current_user.company_id == Activity.company_id).first()

    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if not isInPlanning(activity.planning_id, current_user.id, db):
        raise HTTPException(status_code=404, detail="Join planning '" + str(activity.planning_id) + "' first")

    new_participant = ActivityParticipants(
        activity_id=activity_id,
        user_id=current_user.id
    )
    db.add(new_participant)
    db.commit()
    return {"message": "User joined activity successfully"}


@router.post("/activity_add/{activity_id}/{user_id}")
def add_activity(activity_id: int, user_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    activity = db.query(Activity).filter(Activity.id == activity_id,
                                         current_user.company_id == Activity.company_id).first()

    if current_user.role_id != 2 or current_user.id != activity.creator_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if activity is None:
        print("activity not found")
        raise HTTPException(status_code=404, detail="Activity not found")

    if not isInPlanning(activity.planning_id, user_id, db):
        raise HTTPException(status_code=401,
                            detail="Please add user to planning '" + str(activity.planning_id) + "' first")

    new_participant = ActivityParticipants(
        activity_id=activity_id,
        user_id=user_id
    )
    db.add(new_participant)
    db.commit()
    return {"message": "User added to activity successfully"}


@router.delete("/leave/activity/{activity_id}")
def leave_activity(activity_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    activity = db.query(Activity).filter(Activity.id == activity_id,
                                         current_user.company_id == Activity.company_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    participant = db.query(ActivityParticipants).filter(ActivityParticipants.activity_id == activity_id,
                                                        ActivityParticipants.user_id == current_user.id).first()

    if participant is None:
        raise HTTPException(status_code=404, detail="User not in activity")

    db.delete(participant)
    db.commit()
    return {"message": "User left activity successfully"}


@router.delete("/kick/{activity_id}/{user_id}")
def kick_activity(user_id: int, activity_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    activity = db.query(Activity).filter(Activity.id == activity_id,
                                         current_user.company_id == Activity.company_id).first()
    if current_user.role_id != 2 or current_user.id != activity.creator_id:
        raise HTTPException(status_code=401, detail="Unauthorized")


    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    participant = db.query(ActivityParticipants).filter(ActivityParticipants.activity_id == activity_id,
                                                        ActivityParticipants.user_id == user_id).first()
    if participant is None:
        raise HTTPException(status_code=404, detail="User not in activity")

    db.delete(participant)
    db.commit()
    return {"message": "User kicked from activity successfully"}


def isCompanyPlanning(planning_id: int, company_id: int, db: Session):
    planning = db.query(Planning).filter(
        Planning.id == planning_id,
        Planning.company_id == company_id
    ).first()
    return planning is not None


def isInPlanning(planning_id: int, user_id: int, db: Session):
    print(planning_id, user_id)
    planning = db.query(PlanningParticipant).filter(
        PlanningParticipant.planning_id == planning_id,
        PlanningParticipant.user_id == user_id
    ).first()
    return planning is not None
