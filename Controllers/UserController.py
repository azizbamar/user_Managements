from Controllers.RoleController import getRoleByName
from Controllers.TokenController import checkAccessToken, createAccessToken,createAccessTokenPhone, createAccessTokenWithoutPhone
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Hasher import hash_password,verify_password
from Schemas.Registration import Registration
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.Token import Token
from models.User import User,user_roles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from fastapi import FastAPI,Depends,HTTPException,Header
from Schemas.UserSchema import UserSchema
from models.Role import Role
from models.Phone import Phone
from jose import jwt,JWTError

# sign Up
def signUp(request : Registration ,db):
    try:       
        hashed_password = hash_password(request.password)
        listRolesNames=request.roles
        listRoles=list()
        for role in listRolesNames  :
            print(getRoleByName(db,role))
            listRoles.append(getRoleByName(db,role))

        user = User(email = request.email , password = hashed_password, name = request.name ,telephoneNumber = request.telephoneNumber,roles=listRoles)        
        print(user.telephoneNumber)
        db.add(user)
        db.commit() 
        return {"detail":"register succedded"}
    except IntegrityError as e:
        raise HTTPException(status_code=400,detail="email already in use")
    except FlushError as e:
        raise HTTPException(status_code=400,detail="role not found")
#UPDATE ACCOUNT
def updateUser(request : Registration,token , db):
    try:
        user = checkAccessToken(token)
        print(user.id)
        if (user):
            user = db.query(User).filter(User.id == user.id).first()
            user.password = hash_password(request.password)
            user.name = request.name
            listRolesNames=request.roles
            listRoles=list()
            for role in listRolesNames  :
                listRoles.append(getRoleByName(db,role))
            user.roles = listRoles
            user.telephoneNumber = request.telephoneNumber
            db.commit()
            return "account updated"
        else :
            raise HTTPException(status_code=400,detail="invalid token")    
    except JWTError as e:
        raise HTTPException(status_code=400,detail="Error has been occured : " +e)
#login for guests and web application
def signIn(request : Authentification , db):
 try :   
   user = db.query(User).filter(User.email == request.email).first()
   if (user):
        token=createAccessToken(user,request.password,db)
        return  token
   else:
        raise HTTPException(status_code=400,detail="wrong email or password")
 except ValueError as ve:
    raise HTTPException(status_code=422,detail=str(ve))

def signOut(db,token):
    try:
        db.query(Token).filter(Token.token == token).delete()
        db.commit()
        return {"detail" : "sign out successful"}
    except JWTError as e:
        raise HTTPException(status_code=400 , detail="token not found")
#login for phones
def signInFromPhone(request :PhoneAuthentification  , db):
        user = db.query(User).filter(User.email == request.email).first()
        if (user):
            if not (request.rememberME):
                return createAccessTokenWithoutPhone(user,request.password,db)
            else:
                token=createAccessTokenPhone(user,request.password,request.phone,db)
                return token
        else:
            raise HTTPException(status_code=400,detail="wrong email or password")
        
#phone logout
def signOutFromPhone(db,token):
    try:
        phone = db.query(Phone).filter(Phone.phoneToken == token).first()
        if (phone.uid != None):

            phone.phoneToken = None
            db.commit()
        else:
            db.query(Phone).filter(Phone.phoneToken == token).delete()
            db.commit()
        return {"detail":"sign out succedded"}
    except Exception:
        raise HTTPException(status_code=404,detail="token not found")
    
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
      


 
