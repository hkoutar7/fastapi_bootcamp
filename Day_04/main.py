from fastapi import FastAPI, APIRouter, HTTPException, status

from app.model.UserModel import UserModel
from app.router.UserRouter import router as user_router
from app.router.AuthRouter import router as auth_router
from database.database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI()



app.include_router(user_router)
app.include_router(auth_router)