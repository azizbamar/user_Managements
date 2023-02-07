import re
from pydantic import BaseModel,EmailStr,validator
from typing import Optional
import phonenumbers

class Registration(BaseModel):
    email: EmailStr
    password: str
    name: str
    telephoneNumber: Optional[str]
    roles:Optional[list]=[]
    
    @validator("telephoneNumber")
    def phone_validation(cls, v):
        my_number = phonenumbers.parse(v)
        if not phonenumbers.is_valid_number(my_number):
            raise ValueError("Phone Number Invalid.")
        else:
            return v
#        regex = r'^(?:\+?216)?[07]\d{9,8}$'
#        if v and not re.search(regex, v, re.I):
#            raise ValueError("Phone Number Invalid.")
#        return v