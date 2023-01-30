from pydantic import BaseModel


class AccountUpdate(BaseModel):
    password : str
    telephoneNumber : str