import os
import json
import logging
from typing import Dict, Any, Optional
from google import adk
from app.config import settings
from app.mcp.server import mcp  # Direct access to the FastMCP instance and its tools
from app.schemas.responses import ProblemDetail, PatternDetectionResponse, ComplexityEstimationResponse, LayeredHintResponse, VisualizeResponse

logger = logging.getLogger(__name__)

class DSAMentorAgent:
    def __init__(self):
        """
        Initializes the DSA Mentor Agent using Google ADK.
        It orchestrates the mandated sequence of educational analysis tools.
        """
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
            
        # Initialize the ADK Agent
        # We define a strong educational instruction
        instruction = """
        You are an expert Data Structures and Algorithms mentor and whiteboard teacher.
        Your goal is to guide students through algorithmic thinking and problem-solving.
        
        Focus strictly on: Arrays, Sliding Window, and Two Pointers.
        Languages supported: Java and Python.
        
        Your teaching philosophy:
        - Teach algorithmic thinking and the "thought process."
        - Explain WHY patterns (like Sliding Window) fit a specific problem.
        - Explain invariant maintenance clearly.
        - Never immediately provide full optimized solutions unless explicitly requested.
        - Encourage independent reasoning through layered hints.
        - Be encouraging, precise, and educationally rigorous.
        """
        
        self.agent = adk.Agent(
            name="dsa_mentor_agent",
            model="gemini-2.0-flash", # Using flash for speed and cost-effectiveness
            instruction=instruction
        )
        
        # In a real ADK setup, we would register MCP tools here.
        # Since we are orchestrating them manually for this MVP to ensure strict sequencing,
        # we will use the existing service-level logic or direct tool calls.
        
        logger.info("DSAMentorAgent: Initialized successfully.")

    async def orchestrate(self, url: str, code: str, language: str) -> Dict[str, Any]:
        """
        Orchestrates the mandatory sequence:
        1. fetch_problem
        2. detect_pattern
        3. estimate_complexity
        4. generate_hints
        5. generate_visual_steps
        """
        logger.info(f"DSAMentorAgent: Starting orchestration for URL: {url}")
        
        try:
            # 1. Fetch Problem
            # We call the tool function directly from our mcp server module
            # since they are defined as async functions.
            from app.mcp.server import fetch_problem, detect_pattern, estimate_complexity, generate_hints, generate_visual_steps
            
            problem_data = await fetch_problem(url)
            if "error" in problem_data:
                raise ValueError(f"Failed to fetch problem: {problem_data['error']}")
            
            # 2. Detect Pattern
            pattern_analysis = await detect_pattern(problem_data, code)
            
            # 3. Estimate Complexity
            complexity_analysis = await estimate_complexity(code)
            
            # 4. Generate Hints
            hints = await generate_hints(problem_data, code)
            
            # 5. Generate Visual Steps
            visualization = await generate_visual_steps(problem_data, code)
            
            # Consolidate into the required output format
            result = {
                "problem": problem_data,
                "pattern_analysis": pattern_analysis,
                "complexity_analysis": complexity_analysis,
                "hints": hints,
                "visualization": visualization
            }
            
            logger.info("DSAMentorAgent: Orchestration complete.")
            return result
            
        except Exception as e:
            logger.exception(f"DSAMentorAgent: Orchestration failed: {str(e)}")
            return {"error": str(e), "status": "failed"}

# Instantiate a global agent instance
dsa_mentor_agent = None

def get_agent():
    global dsa_mentor_agent
    if dsa_mentor_agent is None:
        dsa_mentor_agent = DSAMentorAgent()
    return dsa_mentor_agent
