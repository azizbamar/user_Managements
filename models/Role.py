from pydantic import BaseModel
from database.database import  Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from models.User import user_roles,User
from models.RoleClaim import role_claim
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer,primary_key= True , index=True)
    name = Column(String(255),unique= True)
    users = relationship("User", secondary=user_roles,back_populates="roles")
    claims = relationship('Claim', secondary=role_claim,back_populates='roles')