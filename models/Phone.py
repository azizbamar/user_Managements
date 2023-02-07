from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Phone(Base):
    __tablename__ = "phone"
    id = Column(Integer , primary_key= True , index= True)
    uid = Column(String(255) ,unique = True, nullable= True)
    modele=Column(String(255),nullable= True)
    osVersion=Column(String(255),nullable=True)
    phoneToken = Column(String(255),unique=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete = 'CASCADE'), unique=True)
    user = relationship("User", back_populates="phone")
    