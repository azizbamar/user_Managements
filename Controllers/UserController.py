from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
import smtplib
import ssl
import string
from Controllers.RoleController import getRoleByName, getUserRolesById
from Controllers.TokenController import checkAccessToken, createAccessToken,createAccessTokenPhone,get_user
from Controllers.send_email import send_email
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Hasher import hash_password,verify_password
from Schemas.Registration import Registration
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.database import SessionLocal
from models.Token import Token
from models.User import User

from models.Role import Role
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from fastapi import FastAPI,Depends,HTTPException,Header
from Schemas.UserSchema import UserSchema
from Schemas.UpdateUserSchema import UpdateSchema
from models.Phone import Phone
from jose import jwt,JWTError
from errors import *
import asyncio
from fastapi.responses import JSONResponse

from typing import List
from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from confEmail import *
# sign Up
def signUp(request : Registration ,db):
    try:       
        print(request.authorization)
        pwd=generate_password(16)
        import pdb; pdb.set_trace()

        print(pwd)
        hashed_password = hash_password(pwd)
        role = getRoleByName(db,request.role)
        print(role.name)
        user = User(email = request.email , password = hashed_password, name = request.name ,phoneNumber = request.phoneNumber,role=role,authorization=request.authorization)        
        print(user.phoneNumber)
        db.add(user)
        db.commit() 
        subject='Account registred'
        body='Email : '+request.email +'\nPassword : '+pwd
        send_email(request.email,subject,body)
        return {"detail":"register succedded"}
    except IntegrityError as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="email already in use")
    except FlushError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail="role not found")
#UPDATE ACCOUNT
def updateUser(request :Registration,token , db):
    try:
        user = checkAccessToken(token)
        print(user.id)
        if (user):
            user = db.query(User).filter(User.id == user.id).first()
            
            user.password = hash_password(request.password)
            user.name = request.name
 
            user.role = request.role
            user.phoneNumber = request.phoneNumber
            db.commit()
            return "account updated"
        else :
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="invalid token")    
    except JWTError as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been occured : " +e)

from sqlalchemy.exc import SQLAlchemyError


def adminUpdateUser(id, db: Session, request: UpdateSchema, token: str = Header(...)):
    try:
        print('rr')
        if not isinstance(token, str):
            print('ee')
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
     
        if isAdmin(db, token):
            
          
            user = db.query(User).filter(User.id == id).first()

            if user:
            
                
                user.name = request.name  
                user.authorization = request.authorization

                role = db.query(Role).filter(Role.name == request.role).first()
                user.role_id = role.id
                user.phoneNumber = request.phoneNumber
                db.commit()

                return "account updated"
            else:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Access denied"
            )
            
    except JWTError as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"JWTError has been occurred: {e}"
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"SQLAlchemyError has been occurred: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error has been occurredddd: {e}"
        )    



def generate_password(length: int = 10):

    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password
def isAdmin(db: Session, token: str):
    try:
        user = checkAccessToken(token)
        role_id=user["user"].role_id
        
        role = db.query(Role).filter(Role.name == 'admin').first()
        
        if role:
            verif = role_id==role.id
            return bool(verif)
        else:
            return False
    except Exception:
        return False

#login for guests and web application
def signIn(request : Authentification , db):
 try :   
   user = db.query(User).filter(User.email == request.email).first()
   if (user):
        token=createAccessToken(user,request.password,db)
        return  token
   else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="wrong email or password")
 except ValueError as ve:
    raise HTTPException(status_code=422,detail=str(ve))

def getAllUsers(limit:int,db:Session,page:int=1):
    try:
        offset = (page - 1) * limit
        users= db.query(User).offset(offset). limit(limit).all()
        listUsers=list()
        for i in users:
            d=dict()
            if(getUserRolesById(i.id,db)==None):
                     print('i1')
                     d.update({
                    'id':i.id,
                    'email':i.email,
                    'name':i.name,
                    'avatar':i.avatar,
                    'phoneNumber':i.phoneNumber,
                    'role':'None',
                    'authorization':i.authorization
                    }
                    )

            else:
                d.update(
                    {
                    'id':i.id,
                    'email':i.email,
                    'name':i.name,
                    'avatar':i.avatar,
                    'phoneNumber':i.phoneNumber,
                    'role':getUserRolesById(i.id,db),
                    'authorization':i.authorization
                    }
                    )

            listUsers.append(d)
            
            

        return listUsers
    except Exception:
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  





def signOut(db,token):
    try:
        db.query(Token).filter(Token.token == token).delete()
        db.commit()
        return {"detail" : "sign out successful"}
    except JWTError as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST , detail="token not found")
#login for phones
def signInFromPhone(request :PhoneAuthentification  , db):
        user = db.query(User).filter(User.email == request.email).first()
        if (user):
            token=createAccessTokenPhone(user,request.password,request.phone,request.rememberME,db)
            return {"access_token" : token}
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="wrong email or password")
        
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
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail="token not found")
    

    
#filtration par Name
def getUsesrByName(name,db):
    try:
      users=db.query(User).filter(User.name== name).all()
      print(users)
      lusers= list()
      lusers.append(users) 
      return lusers
    except AttributeError as e:
        raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="User not found") 
    except Exception as e:    
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  

    
# remove a phone from user
def removePhoneForUser(user_id,db):

    try:
      db.query(Phone).filter(Phone.user_id == user_id).delete()
      db.commit()
      return dict({"detail":"Phone deleted"})
    except AttributeError as e:
        raise HTTPException (status_code=HTTP_404_NOT_FOUND,detail="User not found") 
    except Exception as e:    
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  

def deleteUser(user_id: int, db: Session):
    try:
        # Check if the user has any roles
   
  
            # Delete the user's roles first
        db.commit()
        print('hamdoulah version 1')
        # Delete the user
        db.query(User).filter(User.id == user_id).delete()
        db.commit()
        
        return {"detail": "User deleted"}
    except AttributeError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while deleting user")

#RESET PASSWORD
def resetPassword(email,db):
    try:
        user = db.query(User).filter(User.email == email).first()
        if (user):
            pwd=generate_password(16)
            subject='your new password'
            body='there is ur new password \npwd: '+pwd

            try:
                user.password = hash_password(pwd)
                db.commit()
                send_email(user.email,subject,body)
                return {'detail : password reset successfully'}
            except:
                raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR , detail="database error")
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND , detail= "user not found")
    except Exception :
        raise HTTPException(status_code= HTTP_500_INTERNAL_SERVER_ERROR , detail= "Error has been occured")








