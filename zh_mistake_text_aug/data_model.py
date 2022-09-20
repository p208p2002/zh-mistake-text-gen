from pydantic import BaseModel
from typing import Optional

class NoiseCorpus(BaseModel):
    type: Optional[str] = None
    correct: str
    incorrect: str
    