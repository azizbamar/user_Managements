
from fastapi import HTTPException
from flask import session


from database.database import SessionLocal
from models.Role import Role
from sqlalchemy.exc import IntegrityError
import json
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from errors import *
from models.User import User
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
        raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="claims id not found") 
    except ValueError as ve:
     raise HTTPException(status_code=422,detail=str(ve))
    except Exception as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been occured" + e) 

def get_role(role_id,db):
   try : 
    if(role_id):
        
        role = db.query(Role).get(role_id)
        return role
    return None

    
   except AttributeError as e:
        raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="role not found") 
   except Exception as e:
        # Handle the error
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  


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
           raise HTTPException(status_code=HTTP_404_NOT_FOUND , detail="role not found")
    except Exception as e:
       raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR , detail="Error has been occured" + e)

def delete_role(role_id,db):
    try :
        role=get_role(role_id,db) 
        db.delete(role)
        db.commit()
        return dict({"detail":"Role deleted"})
    except AttributeError as e:
        raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="role not found")  
    except Exception as e:
        # Handle the error
        db.rollback()
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")        

def getRoleByName(db,name):
   try: 
    return db.query(Role).filter(Role.name == name).first()
   except Exception :
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  


#find By User Id
def getUserById(id_user,db):
    try:
      user=  db.query(User).filter(User.id== id_user).first()
      return user  
    except AttributeError as e:
        raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="User not found") 
    except Exception as e:    
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  

def getUserRolesById(user_id,db:Session):
        try :
            user=getUserById(user_id,db)
            role=get_role(user.role_id,db)
            if role:
                return role.name
            else :return None
            
        except AttributeError as e:
            raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="user not found")  
        except Exception as e:
        # Handle the error
         db.rollback()
         raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")   


        





     






def getAllRoleNames(db):
    try:
        roles= db.query(Role).all()
        listRoles= list(roles)
        listRolesName=list()
        for role in listRoles:
            listRolesName.append(role.name)
        return listRolesName
    except Exception:
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  