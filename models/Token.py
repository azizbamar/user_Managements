from pydantic import BaseModel
from database.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship


class Token(Base):
    __tablename__ = "tokens"
    token = Column(String(255),primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete = 'CASCADE'))
    user = relationship("User", back_populates="tokens")

class PhoneToken(Token):
    __tablename__ = "phonetokens"
    token = Column(String(255),ForeignKey("tokens.token"),primary_key = True)
    phone_id = Column(String(255),unique=True)




