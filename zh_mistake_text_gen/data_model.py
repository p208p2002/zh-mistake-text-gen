from typing import Optional
from pydantic import BaseModel

class NoiseCorpus(BaseModel):
    """
    output format
    """
    type: Optional[str] = None
    correct: str
    incorrect: str
    