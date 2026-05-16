from fastapi import APIRouter
from app.schemas.requests import SimilarRequest
from app.schemas.responses import SimilarResponse

router = APIRouter()

@router.post("/", response_model=SimilarResponse)
async def recommend_similar(request: SimilarRequest):
    # Placeholder for recommendation logic
    return {
        "recommendations": [
            {
                "title": "Longest Substring Without Repeating Characters",
                "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
                "difficulty": "Medium"
            }
        ]
    }
