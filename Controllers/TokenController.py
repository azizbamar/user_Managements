from Schemas import Hasher
import bcrypt,time
from fastapi import FastAPI, HTTPException, Depends,Header
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import jwt
from models.Token import Token
def createAccessToken(user,password,db):
    if (user):
        payload ={
            "email" : user.email,
            "expires" : time.time()+600
        }
        if Hasher.verify_password(password, user.password):
            access_token = jwt.encode(payload, "secret", algorithm="HS256")
            token = Token(token = access_token , user = user)
            db.add(token)
            db.commit()
            return {"access_token": access_token, "token_type": "Bearer"}
        else:
            raise HTTPException(status_code=400, detail="wrong email or password")


async def checkAccessToken(token : str = Header(...)):
    try:
        decoded_token = jwt.decode(token, "secret",algorithms=['HS256'])
        return decoded_token
    except jwt.DecodeError:
        raise HTTPException(status_code=400,detail="invalid token")

async def invalidateToken(token : str = Header(...)):
    try:
        decoded_token = jwt.decode(token, "secret",algorithms=['HS256'])
        if (decoded_token):
            return "logout successfully"
    except jwt.DecodeError:
        raise HTTPException(status_code=400,detail="invalid token")