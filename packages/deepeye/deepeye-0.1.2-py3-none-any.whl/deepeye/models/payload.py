from pydantic import BaseModel
from typing import List


class Payload(BaseModel):
    data: List[float]
    model_path: str
    max_value: int
    up_scale: int
