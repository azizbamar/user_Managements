from pydantic import BaseModel
class Authentification(BaseModel):
    email : str
    password : str