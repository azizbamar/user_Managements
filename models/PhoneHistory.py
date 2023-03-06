from sqlalchemy import Column,Integer,String,ForeignKey
from database.database import Base

class PhoneHistory(Base):
    __tablename__ = "phoneshistory"
    id = Column(Integer , primary_key= True , index= True)
    uid = Column(String(255) , nullable= True)
    model=Column(String(255),nullable= True)
    osVersion=Column(String(255),nullable=True)
    phoneToken = Column(String(255),unique=True)    
