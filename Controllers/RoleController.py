
from fastapi import HTTPException
from flask import session
from Schemas.RoleSchema import RoleSchema


from database.database import SessionLocal, get_table_names
from models.Role import Role
from sqlalchemy.exc import IntegrityError
import json
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from errors import *
from models.User import User
def add_role(role:RoleSchema,db):
    try:
   
        role = Role(name=role.name,claims=role.claims,color=role.color,tags=role.tags)
        db.add(role)
        db.commit()
        return dict({"detail":"register succedded"})
    except IntegrityError as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=HTTP_409_INTERNAL_SERVER_ERROR,detail="color or name already exist") 
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
        role = get_role(role_id,db)
     
        if (role):
            print(role)
            role.name = r.name
            role.claims = r.claims
            role.tags=r.tags
            db.commit()
            return "role updated successfully"
        else:
           raise HTTPException(status_code=HTTP_404_NOT_FOUND , detail="role not found")
    except IntegrityError as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=HTTP_409_INTERNAL_SERVER_ERROR,detail="name already in use")
    except Exception as e:
       raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR , detail="Error has been occured" + e)

def delete_role(role_id,db):
    try :
        try:
            role=get_role(role_id,db)
            db.delete(role)
            db.commit()
        except Exception as e:
            raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  
        return dict({"detail":"Role deleted"})
    except Exception as e:
        db.rollback()
        raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="role not found")
         
def getRoleByName(db,name):
   role = db.query(Role).filter(Role.name == name).first()
   if (role):
        return role
   else:
        raise  HTTPException (status_code=HTTP_404_NOT_FOUND,detail="role not found")  

def getRoleClaimsKeys(db,id):
   try: 
    role= db.query(Role).filter(Role.id == id).first()
    return role.claims
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
                return {"name":role.name,"color":role.color}
            else :
                return None
        except AttributeError as e:
            raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="user not found")  
        except Exception as e:
        # Handle the error
         db.rollback()
         raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")   

def getAllClaims(db: Session):

    listClaims = []
    listObjectNames=get_table_names(db)

    
    for item in listObjectNames:
                if item not in ['tokens','stock','objects','desks','doors']:
                  
                    listClaims.append({'object':item,'rights':''})

    return listClaims




 

def checkinlist(list,name):
    test=False
    for x in list:
      if x['name']==name:
          test=True
    return test
          

def get_all_merged_tags(session):
    all_tags = {}
    roles = session.query(Role).all()
    for role in roles:
        for tag in role.tags:
            key = tag["key"]
            value = tag["value"]
            if key in all_tags and all_tags[key] != value:
                pass
            all_tags[key] = value
    return all_tags











     






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


def getAllRoles(db):
    try:
        roles= db.query(Role).all()
        
        return roles
    except Exception:
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured") 