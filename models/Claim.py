from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base

from models.RoleClaim import role_claim
class Claim(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True,index=True)
    description  = Column(String(255))
    roles = relationship('Role',secondary=role_claim ,back_populates='claims')

    
