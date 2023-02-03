from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,ForeignKey,PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from database.database import Base


class RoleClaim(Base):
    __tablename__ ="role_claim"
    role_id = Column(Integer, ForeignKey('roles.id'))
    claim_id = Column(Integer, ForeignKey('claims.id'))
    PrimaryKeyConstraint(role_id, claim_id)