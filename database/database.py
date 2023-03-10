from sqlalchemy.orm import Session
from sqlalchemy import inspect,text
from typing import List
from fastapi import Depends
from flask import session
from sqlalchemy import create_engine
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Opening JSON file
with open('config.json') as json_file:
    cfg = json.load(json_file)

engine =create_engine(f'mysql+pymysql://{cfg["database"]["user"]}:{cfg["database"]["password"]}@{cfg["database"]["ip"]}:{cfg["database"]["port"]}/{cfg["database"]["dbname"]}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

del cfg

def get_db():
   db=None
   
   try:
       db = SessionLocal()
       yield db
   finally:
       db.close()


def get_table_names(db: Session = Depends(get_db)) -> List[str]:
    inspector = inspect(db.bind)
    print(inspector.get_table_names())
    return inspector.get_table_names()

