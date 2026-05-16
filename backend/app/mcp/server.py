from mcp.server.fastmcp import FastMCP
from app.services.leetcode_service import LeetCodeService
from app.services.ai_service import AIService
from app.config import settings
import logging
import sys

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-server")

# Initialize core services
mcp = FastMCP("DSA Mentor Tools")
leetcode_service = LeetCodeService()
ai_service = AIService()

def validate_startup():
    """
    Validates the MCP server configuration and dependencies on startup.
    Fails early with clear logs if requirements are not met.
    """
    logger.info("Starting MCP server validation...")
    
    # 1. Validate Configuration
    logger.info(f"Environment: {settings.ENV}")
    if not settings.GEMINI_API_KEY:
        logger.error("Startup Failure: GEMINI_API_KEY is missing from configuration.")
        sys.exit(1)
    
    # 2. Validate Gemini Initialization
    if not ai_service.is_ready:
        logger.error("Startup Failure: Gemini client failed to initialize.")
        sys.exit(1)
    logger.info("Gemini client initialized successfully.")

    # 3. Validate MCP Tools
    # Note: tools are registered via decorators, so we check if they are in mcp._tools
    # depending on FastMCP version/implementation details. 
    # Usually we can inspect mcp.list_tools() if it's available or just the internal registry.
    try:
        # For FastMCP, tools are often stored in an internal list/dict
        # We'll log the count of registered tools
        tool_count = len(mcp._tools) if hasattr(mcp, "_tools") else "unknown"
        logger.info(f"Registered {tool_count} MCP tools.")
        
        # Log individual tools if possible
        if hasattr(mcp, "_tools"):
            tool_names = [tool.name for tool in mcp._tools.values()]
            logger.info(f"Loaded tools: {', '.join(tool_names)}")
    except Exception as e:
        logger.warning(f"Could not verify registered tools: {e}")

    logger.info("MCP server startup validation complete.")

@mcp.tool()
async def fetch_problem(url: str) -> dict:
    """
    Extracts problem details from a LeetCode URL.
    
    Args:
        url: The full LeetCode problem URL (e.g., https://leetcode.com/problems/two-sum/)
    """
    try:
        logger.info(f"Tool Call: fetch_problem | URL: {url}")
        problem_data = await leetcode_service.fetch_problem(url)
        return problem_data
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return {"error": str(e), "status": "error"}
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        return {"error": "Internal server error", "status": "error"}

@mcp.tool()
async def analyze_code(problem: dict, code: str, language: str) -> dict:
    """Analyzes the code for mistakes and optimizations."""
    return {"analysis": "Placeholder"}

@mcp.tool()
async def detect_pattern(problem: dict, code: str) -> dict:
    """
    Detects the most likely DSA pattern used or needed in the code.
    Explains WHY the pattern fits the problem.
    """
    try:
        logger.info("Tool Call: detect_pattern")
        result = await ai_service.detect_pattern(problem, code)
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error in detect_pattern: {e}")
        return {"error": str(e)}

@mcp.tool()
async def estimate_complexity(code: str) -> dict:
    """
    Estimates time and space complexity of the student's code and explains WHY.
    """
    try:
        logger.info("Tool Call: estimate_complexity")
        result = await ai_service.estimate_complexity(code)
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error in estimate_complexity: {e}")
        return {"error": str(e)}

@mcp.tool()
async def generate_hints(problem: dict, code: str) -> dict:
    """
    Generates layered hints to guide the student WITHOUT giving away the full solution.
    """
    try:
        logger.info("Tool Call: generate_hints")
        result = await ai_service.generate_hints(problem, code)
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error in generate_hints: {e}")
        return {"error": str(e)}

@mcp.tool()
async def generate_visual_steps(problem: dict, code: str) -> dict:
    """
    Generates structured execution steps for algorithm visualization.
    Focuses on Arrays, Sliding Window, and Two Pointers.
    """
    try:
        logger.info("Tool Call: generate_visual_steps")
        result = await ai_service.generate_visual_steps(problem, code)
        return result.model_dump()
    except Exception as e:
        logger.error(f"Error in generate_visual_steps: {e}")
        return {"error": str(e)}

@mcp.tool()
async def recommend_similar_questions(problem: dict, weaknesses: list) -> dict:
    """Recommends similar practice questions."""
    return {"recommendations": []}

if __name__ == "__main__":
    # Run validation before starting the server
    validate_startup()
    logger.info("Starting FastMCP server...")
    mcp.run()
