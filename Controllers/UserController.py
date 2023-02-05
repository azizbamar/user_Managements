from Controllers.TokenController import createAccessToken,createAccessTokenPhone, invalidateToken
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Hasher import hash_password
from Schemas.Registration import Registration
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.User import User,user_roles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from fastapi import FastAPI,Depends,HTTPException,Header
from Schemas.UserSchema import UserSchema
from models.Role import Role
from models.Phone import Phone
def getRoleByName(db,name):
   try: 
    return db.query(Role).filter(Role.name == name).first()
   except Exception :
        raise  HTTPException (status_code=500,detail="Error has been Occured")  

# sign Up


def signUp(request : Registration ,db):
    try:
        if request.email is None or request.telephoneNumber is None or request.password is None or request.roles is None or request.name is None:
            raise ValueError("all firlds are required")
        
        hashed_password = hash_password(request.password)
        listRolesNames=request.roles
        print(listRolesNames)
        listRoles=list()
        for role in listRolesNames  :
            
            print(getRoleByName(db,role))
            listRoles.append(getRoleByName(db,role))
        print(listRoles)
        user = User(email = request.email , password = hashed_password, name = request.name ,telephoneNumber = request.telephoneNumber,roles=listRoles)
        print(user.roles)
        
        db.add(user)
        db.commit() 
        return {"detail":"register succedded"}
    except IntegrityError as e:
        raise HTTPException(status_code=400,detail="this email is used")
    except FlushError as e:
        raise HTTPException(status_code=400,detail="role not found")
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))

#login for guests and web application

def signIn(request : Authentification , db):
 try :   
   if request.email is None or  request.password is None:
        raise ValueError("all firlds are required") 


   user = db.query(User).filter(User.email == request.email).first()
   if (user):
        token=createAccessToken(user,request.password,db)
        return  token
   else:
        raise HTTPException(status_code=400,detail="wrong email or password")
 except ValueError as ve:
    raise HTTPException(status_code=422,detail=str(ve))



#login for phones

def PhonesignIn(request :PhoneAuthentification  , db):
    try:
        if request.email is None or  request.password is None or request.rememberME is None:
            raise ValueError("all firlds are required") 
        user = db.query(User).filter(User.email == request.email).first()
        if  (user):
                if not (request.rememberME):
                    token=createAccessToken(user,request.password,db)
                    return  token
                else:
                    token=createAccessTokenPhone(user,request.password,request.phone,db)
                    return token
        else:
                raise HTTPException(status_code=400,detail="wrong email or password")

    except ValueError as ve:
     raise HTTPException(status_code=422,detail=str(ve))

#logout

def signOut(db,token):
    return invalidateToken(db,token)

#find By User Id

def getUserById(id_user):
    try:
      user=  db.query(User).filter(User.id== id_user).first()
      return user  
    except AttributeError as e:
        raise HTTPException (status_code=400,detail="User not found") 
    except Exception as e:    
        raise  HTTPException (status_code=500,detail="Error has been Occured")  
    
      
#filtration par Name

def getUsesrByName(name,db):
    try:
      users=db.query(User).filter(User.name== name).all()
      print(users)
      lusers= list()
      lusers.append(users) 
      return lusers
    except AttributeError as e:
        raise HTTPException (status_code=400,detail="User not found") 
    except Exception as e:    
        raise  HTTPException (status_code=500,detail="Error has been Occured")  




# remove a phone from user

def removePhoneForUser(user_id,db):
    try:
      db.query(Phone).filter(Phone.user_id == user_id).delete()
      db.commit()
      
      return dict({"detail":"Phone deleted"})
    except AttributeError as e:
        raise HTTPException (status_code=400,detail="User not found") 
    except Exception as e:    
        raise  HTTPException (status_code=500,detail="Error has been Occured")  
      


 
