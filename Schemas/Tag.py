from typing import List, Dict
from pydantic import BaseModel

class Tag(BaseModel):
    key: str
    value: List[str]