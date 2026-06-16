from pydantic import BaseModel
from typing import List, Optional


# -----------------------
# Request Schema
# -----------------------
class ReviewRequest(BaseModel):
    language: str
    code: str


# -----------------------
# Issue Schema
# -----------------------
class Issue(BaseModel):
    line: Optional[int] = None
    title: str
    severity: str
    explanation: str
    fix: str


# -----------------------
# Suggestion Schema
# -----------------------
class Suggestion(BaseModel):
    title: str
    description: str


# -----------------------
# Response Schema
# -----------------------
class ReviewResponse(BaseModel):
    review_id: int
    language: str

    quality_score: int
    security_score: int
    performance_score: int

    issues: List[Issue]
    suggestions: List[Suggestion]

    original_code: str
    improved_code: str

    status: str