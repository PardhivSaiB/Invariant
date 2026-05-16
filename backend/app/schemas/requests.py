from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class AnalysisRequest(BaseModel):
    leetcode_url: str = Field(..., description="The full LeetCode problem URL")
    language: str = Field(..., description="The programming language (java or python)")
    code: str = Field(..., description="The student's code to analyze")

class HintRequest(BaseModel):
    problem_id: str
    code: str
    language: str

class VisualizeRequest(BaseModel):
    problem_id: str
    code: str
    language: str

class SimilarRequest(BaseModel):
    problem_id: str
    weaknesses: Optional[list] = None
