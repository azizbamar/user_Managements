from pydantic import BaseModel

class Registration(BaseModel):
    email : str
    password : str
    name : str
    telephoneNumber : str
    roles:list