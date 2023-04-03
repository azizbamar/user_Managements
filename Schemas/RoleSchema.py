from pydantic import BaseModel
from typing import Any


class RoleSchema(BaseModel):
    name :str
    claims:list
    color:str=None
    tags:Any

