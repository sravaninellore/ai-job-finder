from typing import List
from pydantic import BaseModel

class EligibilityResult(BaseModel):
    eligible: bool
    reasons: List[str] = []
    warnings: List[str] = []
