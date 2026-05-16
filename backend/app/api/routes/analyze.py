from fastapi import APIRouter, HTTPException, Depends
from app.schemas.requests import AnalysisRequest
from app.schemas.responses import OrchestrationResponse
from app.agents.agent import get_agent
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=OrchestrationResponse)
async def analyze_code(request: AnalysisRequest, agent=Depends(get_agent)):
    """
    Analyzes the student's code for a given LeetCode problem.
    Executes the full educational orchestration flow.
    """
    logger.info(f"API Call: POST /analyze | URL: {request.leetcode_url} | Language: {request.language}")
    
    try:
        # Validate language
        if request.language.lower() not in ["java", "python"]:
            raise HTTPException(status_code=400, detail="Unsupported language. Use 'java' or 'python'.")
            
        # Invoke the ADK agent orchestration
        result = await agent.orchestrate(
            url=request.leetcode_url,
            code=request.code,
            language=request.language
        )
        
        # Check for orchestration failures
        if "error" in result:
            logger.error(f"Orchestration failed: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in /analyze: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred during analysis.")
