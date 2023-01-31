from Schemas import Hasher
import bcrypt,time
from fastapi import FastAPI, HTTPException, Depends,Header
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import jwt
from sqlalchemy import exc
from models.Phone import Phone
from models.Token import Token

def createAccessToken(user,password,clientType,phoneId,db):
    payload =createPayload(user)
    if Hasher.verify_password(password, user.password):
        access_token = jwt.encode(payload, "secret", algorithm="HS256")
        if (clientType == "web"):
            token = Token(token = access_token ,clientType = clientType, user = user)
        else:
            createTokenIfNotExist(phoneId,user,db)         
        tokenExist = db.query(Token).filter(Token.phoneId == phoneId).first()
        if not (tokenExist):
            token = Token(token = access_token ,clientType = clientType,phoneId =phoneId, user = user)
        else:
            raise HTTPException(status_code=400,detail="already connected")

        try:
            db.add(token)
            db.commit()
        except exc.IntegrityError as e:
            raise HTTPException(status_code=400,detail="error has been occured")

        return {"access_token": access_token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=400, detail="wrong email or password")


async def checkAccessToken(db,token : str = Header(...)):
    tokenExist = db.query(Token).filter(Token.token == token).first()

    try:
        decoded_token = jwt.decode(token, "secret",algorithms=['HS256'])
        tokenExist = db.query(Token).filter(Token.token == token).first()
        if (tokenExist):
            return decoded_token
        else:
            raise HTTPException(status_code=400,detail="unauthorized")

    except jwt.DecodeError:
        raise HTTPException(status_code=400,detail="invalid token")





def invalidateToken(db,token):
    try:
        decoded_token = jwt.decode(token, "secret",algorithms=['HS256'])
        if (decoded_token):
            print(token)
            db.query(Token).filter(Token.token == token).delete()
            db.commit()
    except jwt.DecodeError:
        raise HTTPException(status_code=400,detail="invalid token")


def createTokenIfNotExist(phoneId,user,db):
    phoneExist = db.query(Phone).filter(Phone.uid == phoneId).first()
    if not (phoneExist):
        phone = Phone(uid = phoneId,user = user)
        db.add(phone)
        db.commit()

def createPayload(user):
    return {
            "email" : user.email,
            "expires" : time.time()+600
        }