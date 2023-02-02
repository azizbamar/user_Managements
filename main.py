from fastapi import FastAPI,Depends,HTTPException
from database.database import engine,SessionLocal,Base
from models.User import User
from models.Token import Token
from models.Phone import Phone
from models.Role import Role
from fastapi.middleware.cors import CORSMiddleware



from sqlalchemy.orm import Session
from Roots.UserRoot import userRooter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(userRooter)

