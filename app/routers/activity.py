from datetime import datetime
from db.db_inc import engine
from fastapi import APIRouter, HTTPException, Depends
from modeles.activity import Activity, ActivityCreate, ActivityParticipants, userJoinActivity
from modeles.user import User
from routers.login import get_current_user
from sqlalchemy.orm import sessionmaker
from utils.admin import is_admin, is_maintainer
from utils.activity import isCompanyPlanning, isInPlanning, isInActivity

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/activities")
def read_activities(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    if is_maintainer(current_user):
        activities = db.query(Activity).all()
    else:
        activities = db.query(Activity).filter(current_user.company_id == Activity.company_id).all()
        if len(activities) == 0:
            raise HTTPException(status_code=404, detail="Activities not found")
    return activities


@router.get("/activity/{activity_id}")
def read_activity(activity_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    if is_maintainer(current_user):
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
    else:
        activity = db.query(Activity).filter(Activity.id == activity_id,
                                             current_user.company_id == Activity.company_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/activity/{planning_id}")
def create_activity(planning_id: int, activity: ActivityCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    if is_maintainer(current_user):
        if not isCompanyPlanning(planning_id, activity.company_id, db):
            raise HTTPException(status_code=422, detail="Not a company planning")
        if current_user.id != activity.creator_id:
            raise HTTPException(status_code=401, detail="Can't create activity for another user")

        new_activity = Activity(
            name=activity.name,
            planning_id=activity.planning_id,
            creator_id=activity.creator_id,
            company_id=activity.company_id,
            date=datetime.today().date(),
            place=activity.place,
            start_time=activity.start_time,
            end_time=activity.end_time,
        )
    else:
        if not isCompanyPlanning(planning_id, current_user.company_id, db):
            raise HTTPException(status_code=422, detail="Not a company planning")
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
    if is_maintainer(current_user):
        activity = db.query(Activity).filter(Activity.id == activity_id).one()
        if activity is None:
            raise HTTPException(status_code=404, detail="Activity not found")
    else:
        activity = db.query(Activity).filter(Activity.id == activity_id,
                                             current_user.company_id == Activity.company_id).one()
        if activity is None:
            raise HTTPException(status_code=404, detail="Activity not found")

        elif activity.creator_id != current_user.id or not is_admin(current_user):
            raise HTTPException(status_code=401, detail="Unauthorized")
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


@router.post("/activity/{activity_id}/join")
def join_activity(activity_id: int, userJoin: userJoinActivity, current_user: User = Depends(get_current_user)):
    if current_user.id != userJoin.user_id and not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized to add user to this activity")

    db = SessionLocal()
    user = db.query(User).filter(User.id == userJoin.user_id).one()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    activity = db.query(Activity).filter(Activity.id == activity_id).one()

    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity.company_id != user.company_id:
        raise HTTPException(status_code=422, detail="User not in this company")

    if is_admin(current_user) and not is_maintainer(current_user):
        if activity.company_id != current_user.company_id:
            raise HTTPException(status_code=422, detail="Not a company activity")

    if not isInPlanning(activity.planning_id, user.id, db):
        raise HTTPException(status_code=404, detail="Join planning '" + str(activity.planning_id) + "' first")

    if isInActivity(activity_id, user.id, db):
        raise HTTPException(status_code=422, detail="User already in activity")

    new_participant = ActivityParticipants(
        activity_id=activity_id,
        user_id=user.id
    )
    db.add(new_participant)
    db.commit()
    return {"message": "User joined activity successfully"}


@router.delete("/activity/{activity_id}/leave/{user_id}")
def leave_activity(activity_id: int, user_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).one()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if is_maintainer(current_user):
        activity = db.query(Activity).filter(Activity.id == activity_id,
                                                                        user.company_id == Activity.company_id).first()
        if activity is None:
            raise HTTPException(status_code=404, detail="Activity not found")

    participant = db.query(ActivityParticipants).filter(ActivityParticipants.activity_id == activity_id,
                                                        ActivityParticipants.user_id == user.id).first()

    if participant is None:
        raise HTTPException(status_code=404, detail="User not in activity")

    db.delete(participant)
    db.commit()
    return {"message": "User left activity successfully"}
