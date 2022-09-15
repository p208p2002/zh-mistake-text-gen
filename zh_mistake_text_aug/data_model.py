from pydantic import BaseModel
from typing import Optional

class NoiseCorpus(BaseModel):
    type: Optional[str] = None
    correct: str
    incorrect: str
    incorrect_start_at: int
    incorrect_end_at: int
    span:str