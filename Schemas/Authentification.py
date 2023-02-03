from pydantic import BaseModel
from typing import Union

class Authentification(BaseModel):
    email : str
    password : str
    #configurer dans angular