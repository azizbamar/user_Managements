from pydantic import BaseModel

class Registration(BaseModel):
    email : str=None
    password : str=None
    name : str=None
    telephoneNumber : str=None
    roles:list=None