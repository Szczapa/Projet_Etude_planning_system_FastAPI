from fastapi import FastAPI
from routers import user, company, role, planning, login
from db.db_inc import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, tags=["users"])
app.include_router(company.router, tags=["companies"])
app.include_router(role.router, tags=["roles"])
app.include_router(planning.router, tags=["plannings"])
app.include_router(login.router, tags=["login"])
