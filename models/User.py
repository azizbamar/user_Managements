from pydantic import BaseModel
from database.database import  Base
from sqlalchemy import Boolean, Column,Integer,String,ForeignKey,Table,ARRAY
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    name = Column(String(255))
    phoneNumber = Column(String(255), unique=True)
    avatar = Column(String(255))
    authorization = Column(Boolean)
    role_id = Column('role_id', Integer, ForeignKey('roles.id'))
    phone = relationship("Phone", uselist=False, back_populates="user", passive_deletes=True)
    tokens = relationship("Token", back_populates="user", passive_deletes=True)
    role = relationship("Role", back_populates="users")
    demandes = relationship("Demand", uselist=False, back_populates="user", cascade="all, delete-orphan")
    desks = relationship("Reservation", back_populates="user")

    
  
    

    


