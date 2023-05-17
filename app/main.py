from fastapi import FastAPI
from routers import user, company, role, planning, login, activity
from db.db_inc import engine, Base
import time

app = FastAPI()

nb_attempts_bd_init = 0


def init_db(nb_attempts_bd_init):
    "will loop during 2 minutes waiting for the database to be in ready state"
    try:
        Base.metadata.create_all(bind=engine)

    except Exception as e:
        nb_attempts_bd_init += 1
        time.sleep(5)
        print(f"db schema init failed, waiting 5 seconds, {nb_attempts_bd_init} attempts so far]")
        if nb_attempts_bd_init < 24:
            init_db(nb_attempts_bd_init)
        else:
            print("Error: ", e)
            print("Waited for more than 2 minutes, db still not init... exiting")
            exit(1)


init_db(nb_attempts_bd_init)

app.include_router(user.router, tags=["users"])
app.include_router(company.router, tags=["companies"])
app.include_router(role.router, tags=["roles"])
app.include_router(planning.router, tags=["plannings"])
app.include_router(login.router, tags=["login"])
app.include_router(activity.router, tags=["activity"])
