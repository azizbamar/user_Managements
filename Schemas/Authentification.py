from pydantic import BaseModel,EmailStr
from typing import Union

class Authentification(BaseModel):
    email : EmailStr
    password : str
