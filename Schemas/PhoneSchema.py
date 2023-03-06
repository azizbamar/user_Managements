from pydantic import BaseModel
class PhoneSchema(BaseModel):
    uid :str
    model:str
    osVersion:str



    