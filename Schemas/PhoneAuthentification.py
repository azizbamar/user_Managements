from pydantic import BaseModel
from typing import Union
from Schemas.PhoneSchema import PhoneSchema
class PhoneAuthentification(BaseModel):
    email : str=None
    password : str=None
    #configurer dans angular
    rememberME : bool=None
    phone :PhoneSchema=None