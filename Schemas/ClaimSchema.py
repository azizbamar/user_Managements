from typing import Optional
from pydantic import BaseModel
class ClaimSchema(BaseModel):
    User :str
    Role :str
    Phone :str
