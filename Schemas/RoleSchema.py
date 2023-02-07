from pydantic import BaseModel
from Schemas.ClaimSchema import ClaimSchema

class RoleSchema(BaseModel):
    name :str
    claims:ClaimSchema

