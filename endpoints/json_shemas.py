from pydantic import BaseModel
from typing import List


class ObjectInfo(BaseModel):
    colors: list
    objects: list


class MemePostPayload(BaseModel):
    id: int
    text: str
    url: str
    tags: List[str]
    updated_by: str
    info: ObjectInfo
