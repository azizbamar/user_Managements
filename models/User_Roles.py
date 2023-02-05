from database.database import  Base
from sqlalchemy import Column,Integer,ForeignKey,Table

user_roles = Table('user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)