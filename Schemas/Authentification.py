from pydantic import BaseModel
from typing import Union

class Authentification(BaseModel):
    email : str=None
    password : str=None
    #configurer dans angular