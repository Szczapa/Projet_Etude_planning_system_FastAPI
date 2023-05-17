from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.company import Company, CompanyCreate
from sqlalchemy.orm import sessionmaker
from routers.login import get_current_user
from modeles.user import User
from sqlalchemy import func
from utils.admin import is_maintainer

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/companies")
def read_companies(current_user: User = Depends(get_current_user)):
    if not is_maintainer(current_user):
        raise HTTPException(status_code=401, detail="Unauthorized")
    db = SessionLocal()
    companies = db.query(Company).all()
    return companies


# @router.get("/companies/{company_id}")
# def read_company(company_id: int):
#     db = SessionLocal()
#     company = db.query(Company).filter(Company.id == company_id).first()
#     return company


@router.post("/company", status_code=201)
def create_company(company: CompanyCreate, current_user: User = Depends(get_current_user)):
    if current_user.role_id != 3:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db = SessionLocal()
    existing_company = db.query(Company).filter(func.lower(Company.name) == func.lower(company.name)).first()
    if existing_company:
        raise HTTPException(status_code=422, detail="Company name already exists")

    new_company = Company(
        name=company.name
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

@router.delete("/company/{company_id}")
def delete_company(company_id: int, current_user: User = Depends(get_current_user)):
    if current_user.role_id != 3:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db = SessionLocal()
    company = db.query(Company).filter(Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)
    db.commit()
    return {"message": "Company deleted successfully"}

@router.put("/company/{company_id}")
def update_company(company_id: int, company: CompanyCreate, current_user: User = Depends(get_current_user)):
    if current_user.role_id != 3:
        raise HTTPException(status_code=401, detail="Unauthorized")

    db = SessionLocal()
    existing_company = db.query(Company).filter(func.lower(Company.name) == func.lower(company.name)).first()
    if existing_company:
        raise HTTPException(status_code=422, detail="Company name already exists")

    company_to_update = db.query(Company).filter(Company.id == company_id).first()
    if company_to_update is None:
        raise HTTPException(status_code=404, detail="Company not found")
    company_to_update.name = company.name
    db.commit()
    return {"message": "Company updated successfully"}