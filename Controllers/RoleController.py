from fastapi import HTTPException
from models.Role import Role
from sqlalchemy.exc import IntegrityError
from Controllers.ClaimController import getClaimById

def CreateListClaims(listIdClaims,db):
        listClaims=list()
        for idClaim in listIdClaims:
            listClaims.append(getClaimById(db,idClaim))
        return listClaims


def add_role(role,db):
    try:
        if role.name is None or  role.claimsId is None  :
            raise ValueError("all firlds are required") 
        listClaimsId=role.claimsId
        lClaims=CreateListClaims(listIdClaims=listClaimsId,db=db)
        role = Role(name=role.name,claims=lClaims)
    
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
        raise HTTPException (status_code=500,detail="Error has been Occured") 


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
        role = get_role(role_id,db)
        if  ( not r.name is  None or not  r.claimsId  is  None):
            if not (r.name is  None):
                role.name=r.name
            if not(r.claimsId is None):
                listClaimsId=r.claimsId
                listClaims=CreateListClaims(listClaimsId,db)
                role.claims=listClaims
            db.commit()
            role =get_role(role_id,db)
            return role
        else :
            return dict({'detail':"No field updated"})
    except AttributeError as e:
        raise HTTPException (status_code=400,detail="role not found") 
 
    except IntegrityError as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=409,detail="claim not found") 
    except Exception as e:
        # Handle the error
        db.rollback()
        return "Error: " + str(e)

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
    