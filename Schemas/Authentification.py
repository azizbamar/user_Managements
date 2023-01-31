from pydantic import BaseModel
from typing import Union

class Authentification(BaseModel):
    email : str
    password : str
    clientType : str
    phoneId :Union[str, None]