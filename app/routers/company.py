from fastapi import APIRouter, status, HTTPException, Response
from db.db_inc import engine, Base
from modeles.company import Company
from sqlalchemy.orm import sessionmaker

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/companies")
def read_companies():
    db = SessionLocal()
    companies = db.query(Company).all()
    return companies


# @router.get("/companies/{company_id}")
# def read_company(company_id: int):
#     db = SessionLocal()
#     company = db.query(Company).filter(Company.id == company_id).first()
#     return company
