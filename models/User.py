from pydantic import BaseModel
from database.database import  Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key = True , index = True)
    email = Column(String(255))
    password = Column(String(255))
    username = Column(String(255))
    telephoneNumber = Column(String(255))
    phone = relationship("Phone", uselist=False, back_populates="user")
    tokens = relationship("Token", back_populates="user")
