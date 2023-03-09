from pydantic import BaseModel
from typing import Any


class RoleSchema(BaseModel):
    name :str
    claims:list

