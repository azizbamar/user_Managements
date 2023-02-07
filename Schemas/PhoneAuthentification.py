from pydantic import BaseModel,EmailStr
from typing import Union
from Schemas.PhoneSchema import PhoneSchema
class PhoneAuthentification(BaseModel):
    email : EmailStr
    password : str
    #configured dans angular
    rememberME : bool
    phone :PhoneSchema
