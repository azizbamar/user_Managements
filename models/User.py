from pydantic import BaseModel
from database.database import  Base
from sqlalchemy import Column,Integer,String,ForeignKey,Table,ARRAY
from sqlalchemy.orm import relationship
from models.User_Roles import user_roles
class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key = True , index = True)
    email = Column(String(255),unique=True)
    password = Column(String(255))
    name = Column(String(255))
    telephoneNumber = Column(String(255)) 
    avatar = Column(String(255)) 
    phone = relationship("Phone", uselist=False, back_populates="user",passive_deletes=True)
    tokens = relationship("Token", back_populates="user",passive_deletes=True)
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    


