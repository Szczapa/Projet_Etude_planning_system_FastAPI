from sqlalchemy.orm import Session
from modeles.planning import Planning, PlanningParticipant
from modeles.activity import ActivityParticipants


def isCompanyPlanning(planning_id: int, company_id: int, db: Session):
    print(planning_id, company_id)
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

def isInActivity(activity_id: int, user_id: int, db: Session):
    print(activity_id, user_id)
    activity = db.query(ActivityParticipants).filter(
        ActivityParticipants.activity_id == activity_id,
        ActivityParticipants.user_id == user_id
    ).first()
    return activity is not None