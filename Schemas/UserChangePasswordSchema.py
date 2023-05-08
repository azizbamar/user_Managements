from pydantic import BaseModel
class UserChangePasswordSchema(BaseModel):
    current_password :str
    new_password :str
 