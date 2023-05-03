from fastapi import FastAPI
from routers import user, company
from db.db_inc import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router, tags=["users"])
app.include_router(company.router, tags=["companies"])