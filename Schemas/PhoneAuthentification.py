from pydantic import BaseModel
from typing import Union
from Schemas.PhoneSchema import PhoneSchema
class PhoneAuthentification(BaseModel):
    email : str
    password : str
    #configurer dans angular
    rememberME : bool
    phone :PhoneSchema=None