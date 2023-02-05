from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,ForeignKey,PrimaryKeyConstraint,Table
from sqlalchemy.orm import relationship

from database.database import Base



role_claim = Table('role_claim', Base.metadata,
    Column('role_id',Integer, ForeignKey('roles.id')),
    Column('claim_id',Integer, ForeignKey('claims.id'))
)