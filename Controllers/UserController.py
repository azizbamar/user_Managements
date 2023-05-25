import io
import secrets
import string
from Controllers.RoleController import getRoleByName, getUserRolesById
from Controllers.TokenController import checkAccessToken, createAccessToken,createAccessTokenPhone
from Controllers.send_email import send_email
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Hasher import hash_password
from Schemas.Registration import Registration
from sqlalchemy.orm import Session
from Schemas.SendEmailsSchema import SendEmails
from models.Notification import Notification
from models.Token import Token
from models.User import User
from models.Role import Role
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from fastapi import HTTPException,Header,Form,UploadFile,File,status
from Schemas.UpdateUserSchema import UpdateSchema
from models.Phone import Phone
from jose import JWTError
from errors import *
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from confEmail import *
import base64
import asyncio
from sqlalchemy.exc import IntegrityError
from PIL import UnidentifiedImageError
from fastapi import Form, HTTPException, UploadFile,File
from io import BytesIO
from PIL import Image, UnidentifiedImageError
# sign Up
def signUp(request : Registration ,db):
    try:       
        pwd=generate_password(16)
        hashed_password = hash_password(pwd)
        role = getRoleByName(db,request.role)
        user = User(email = request.email , password = hashed_password, name = request.name ,phoneNumber = request.phoneNumber,role=role,authorization=request.authorization)        
        db.add(user)
        db.commit() 
        subject='Account registred'
        body='Email : '+request.email +'\nPassword : '+pwd
        send_email(request.email,subject,body)
        return {"detail":"register succedded"}
    
    except IntegrityError as e:
        raise HTTPException(status_code=HTTP_409_INTERNAL_SERVER_ERROR,detail="email or phone number already in use")
    except FlushError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail="role not found")
#UPDATE ACCOUNT
def updateUser(request :Registration,token , db):
    try:
        user = checkAccessToken(token)
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

def updateRight(db:Session,token:str):
    try:
        user = checkAccessToken(token)
        role_id=user["user"].role_id
        
        role = db.query(Role).filter(Role.id == role_id).first()
        test=False
        if role:
            claims=role.claims
            for i in claims:
                if i['object']=='users':
                  if 'u' in  i['rights']:
                    test=True
            verif = test
            return bool(verif)
        else:
            return False
    except Exception:
        return False

def deleteRight(db:Session,token:str):
    try:
        user = checkAccessToken(token)
        role_id=user["user"].role_id
        
        role = db.query(Role).filter(Role.id == role_id).first()
        test=False
        if role:
            claims=role.claims
            for i in claims:
                if i['object']=='users':
                  if 'd' in  i['rights']:
                    test=True
            verif = test
            return bool(verif)
        else:
            return False
    except Exception:
        return False

def adminUpdateUser(id, db: Session, request: UpdateSchema, token: str = Header(...)):
    try:
        if updateRight(db, token):
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
                print('aaaaaaa')
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
    except IntegrityError as e:
        # Handle the error
        db.rollback()
        raise HTTPException (status_code=HTTP_409_INTERNAL_SERVER_ERROR,detail="Phone number already in use")
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


#GENERATE RANDOM PASSWORD
def generate_password(length: int = 10):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def getUserClaims(db: Session, token: str) -> List[str]:
    try:
        user = checkAccessToken(token)
        role_id = user["user"].role_id
        role = db.query(Role).filter(Role.id == role_id).first()
        listclaims=list()
        if role:
            claims=role.claims
            
            for item in claims:
             
             listclaims.append(item['object'])
            print(listclaims)
            return [listclaims,claims]
        else:
            return []
    except Exception:
        return []


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

def displayAdminDashboard(db: Session, token: str):
    try:
        user = checkAccessToken(token)
        role_id=user["user"].role_id
        
        role = db.query(Role).filter(Role.id==role_id).first()
        
        if role:
            test=False
            claims=role.claims
            for elm in claims:
                if 'r' in elm['rights']:
                  test=True
            return {"isAdmin":bool(test),"claims":getUserClaims(db,token)[0],"details":getUserClaims(db,token)[1]}
        else:
            return False
    except Exception:
        return False
    

async def updateAvatar(id,picture,db):
   user = db.query(User).filter(User.id == id).first()
   if user:
    if picture:
        try:
            # Read the image file content
            image_content = await picture.read()

            # Open the image using Pillow
            image = Image.open(io.BytesIO(image_content))

            # Resize the image
            image = image.resize((500, 500))

            # Convert the image to RGB mode
            image = image.convert("RGB")

            # Save the image to a byte stream
            image_byte_array = io.BytesIO()
            image.save(image_byte_array, format='JPEG')

            # Encode the image content in base64
            image_data = base64.b64encode(image_byte_array.getvalue())

            # Decode the base64 string to a regular string
            image_str = image_data.decode('utf-8')

            user.avatar = image_str.encode('utf-8')

        except UnidentifiedImageError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image"
            )

    try:
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="name already exists"
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image")

    return {"message": "Material updated successfully"}




#login for guests and web application
def signIn(request : Authentification , db):
 try :   
   user = db.query(User).filter(User.email == request.email).first()
   if (user):
#         if(user.authorization):
        token=createAccessToken(user,request.password,db)
        return  token
        # else :
        #      raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="This account is blocked")


   else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="wrong email or password")
 except ValueError as ve:
    raise HTTPException(status_code=422,detail=str(ve))



def getuser(email : str , db):
 try :   
   user = db.query(User).filter(User.email == email).first()
   if (user):
       
        return  user
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
            phone=db.query(Phone).filter(Phone.user_id==i.id)
            if(getUserRolesById(i.id,db)==None):
                     d.update({
                    'id':i.id,
                    'email':i.email,
                    'name':i.name,
                    'avatar':i.avatar,
                    'phoneNumber':i.phoneNumber,
                    'phone':phone,
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
                    'phone':phone,
                    'authorization':i.authorization
                    }
                    )
            listUsers.append(d)   
        return listUsers
    except Exception:
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  

def signOut(db,token):
        token = db.query(Token).filter(Token.token == token).first()
        if(token):
            db.delete(token)
            db.commit()
            return {"detail" : "sign out successful"}
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND , detail="token not found")
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
def getUsersByName(name,db):
    users=db.query(User).filter(User.name== name).all()
    lusers= list()
    lusers.append(users) 
    return lusers


    
# remove a phone from user
def removePhoneForUser(user_id,db):
    user = db.query(User).filter(User.id == user_id).first()
    if(user): 
        phone = db.query(Phone).filter(Phone.user_id == user_id).first()
        if(phone):
            db.delete(phone)
            db.commit()
            return dict({"detail":"Phone deleted"})
        else:
            raise HTTPException (status_code=HTTP_401_UNAUTHORIZED,detail="User has not a phone") 
    else:
        raise HTTPException (status_code=HTTP_401_UNAUTHORIZED,detail="User not found") 

def deleteUser(token:str,user_id: int, db: Session):
    try:
        # Check if the user has any roles
   
  
            # Delete the user's roles first
        
        # Delete the user
        if(deleteRight(db,token)):
            user =db.query(User).filter(User.id == user_id).first()
            if(user):
                
                userPhone=db.query(Phone).filter(Phone.user_id==user_id).first()
                print(userPhone)
                if userPhone:
                    userPhone.delete()
                    print('ab')
                   
                userNot= db.query(Notification).filter(Notification.user_id == user_id).first() 
                if  userNot :    
                 print('not')
                 
                 db.query(Notification).filter(Notification.user_id == user_id).delete()    
                print('ha3')
                db.query(User).filter(User.id == user_id).delete()
            print('a')

            
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
        print(user)
        
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

def getAll(db:Session):
    try:
        users= db.query(User).all()
        listUsers=list()
        for i in users:
            try:
                phone=db.query(Phone).filter(Phone.user_id==i.id).one_or_none()
            except:
                raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Phone")
            d=dict()
            if phone:
                  phone_dict = {
                     'id': phone.id,
                     'uid': phone.uid,
                     'model': phone.model,
                     'osVersion': phone.osVersion
                            }
            if(getUserRolesById(i.id,db)==None):
                d.update({
                    'id':i.id,
                    'email':i.email,
                    'name':i.name,
                    'avatar':i.avatar,
                    'phoneNumber':i.phoneNumber,
                    'phone': phone_dict if phone else 'None',
                    'role':'None',
                    'authorization':i.authorization
                })
            else:
                d.update({
                    'id':i.id,
                    'email':i.email,
                    'name':i.name,
                    'avatar':i.avatar,
                    'phoneNumber':i.phoneNumber,
                    'role':getUserRolesById(i.id,db)['name'],
                    'color':getUserRolesById(i.id,db)['color'],
                    'phone': phone_dict if phone else 'None',
                    'authorization':i.authorization
                })
            listUsers.append(d)
        print(listUsers)
        return listUsers
    except Exception:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")

def deletePhoneByPhneNumber(phonenumber,db:Session) :
    try:
      user_id=db.query(User).filter(User.phoneNumber==phonenumber).first().id
      userPhone=db.query(Phone).filter(Phone.user_id==user_id).first()
      if userPhone:
        db.delete(userPhone)
        db.commit()
    except:
      print('An exception occurred')


def deletePhone(id:int,db:Session):
    try:
      db.query(Phone).filter(Phone.id==id).delete()
      db.commit()
      return{"detail":"Phone deleted"}
    except:
      raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")
    

def sendEmails(SendEmailSchema: SendEmails):
    url = "http://localhost:8001/sendEmails/"
    payload = {"emails": SendEmailSchema.recipients, "subject": SendEmailSchema.subject, "body": SendEmailSchema.body}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return {"details": "Email sent successfully"}

from Schemas import Hasher
def change_password(db: Session, user_id: int, password: str, new_password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    pwdCorrect=Hasher.verify_password(password, user.password)
    if not pwdCorrect:
        raise HTTPException(status_code=400, detail="Current password incoreect")
    hashed_password = Hasher.hash_password(new_password)
    user.password = hashed_password
    db.commit()
    return {"message": "Password updated successfully"}