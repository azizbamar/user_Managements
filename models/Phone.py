from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Phone(Base):
    __tablename__ = "phone"
    uid = Column(String(255) ,primary_key = True)
    modele=Column(String(255))
    androidVersion=Column(String(255),nullable=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete = 'CASCADE'), unique=True,nullable = True)
    user = relationship("User", back_populates="phone")
    