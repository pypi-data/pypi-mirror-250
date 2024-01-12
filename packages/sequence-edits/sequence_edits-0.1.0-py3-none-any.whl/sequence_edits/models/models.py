from typing import Literal, TypeVar
from pydantic import BaseModel
import ramda as R

A = TypeVar("A")

Type = Literal["insert", "skip"]
class Edit(BaseModel):
    type: Type
    idx: int
    
def skip(idx: int) -> Edit:
    return Edit(type="skip", idx=idx)

def insert(idx: int) -> Edit:
    return Edit(type="insert", idx=idx)
