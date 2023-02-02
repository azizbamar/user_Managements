from pydantic import BaseModel
class UserSchema(BaseModel):
    email :str
    password :str
    name :str
    telephoneNumber :str 
    avatar :str 