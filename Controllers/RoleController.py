from fastapi import HTTPException
from models.Role import Role
from sqlalchemy.exc import IntegrityError
import json
from fastapi.encoders import jsonable_encoder

def add_role(role,db):
    try:
        role = jsonable_encoder(role)
        role = Role(name=role['name'],claims=json.dumps(role['claims']))
        db.add(role)
        db.commit()
        return dict({"detail":"register succedded"})
    except IntegrityError as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=409,detail="claims id not found") 
    except ValueError as ve:
     raise HTTPException(status_code=422,detail=str(ve))
    except Exception as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=500,detail="Error has been occured" + e) 

def get_role(role_id,db):
   try : 
    role = db.query(Role).get(role_id)
    return role
   except AttributeError as e:
        raise HTTPException (status_code=400,detail="role not found") 
   except Exception as e:
        # Handle the error
        raise  HTTPException (status_code=500,detail="Error has been Occured")  


def update_role(r, role_id,db):
    try:
        r = jsonable_encoder(r)
        role = get_role(role_id,db)
        print(role)
        print(r)
        if (role):
            role.name = r['name']
            role.claims = r['claims']
            db.commit()
            return "role updated successfully"
        else:
           raise HTTPException(status_code=404 , detail="role not found")
    except Exception as e:
       raise HTTPException(status_code=400 , detail="Error has been occured" + e)

def delete_role(role_id,db):
    try :
        role=get_role(role_id,db) 
        db.delete(role)
        db.commit()
        return dict({"detail":"Role deleted"})
    except AttributeError as e:
        raise HTTPException (status_code=400,detail="role not found")  
    except Exception as e:
        # Handle the error
        db.rollback()
        raise  HTTPException (status_code=500,detail="Error has been Occured")        

def getRoleByName(db,name):
   try: 
    return db.query(Role).filter(Role.name == name).first()
   except Exception :
        raise  HTTPException (status_code=500,detail="Error has been Occured")  