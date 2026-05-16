import os
import json
import logging
import re
from typing import Dict, Any, Type, TypeVar, Optional, Union
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.config import settings
from app.schemas.responses import (
    PatternDetectionResponse, 
    ComplexityEstimationResponse, 
    LayeredHintResponse,
    VisualizeResponse
)

logger = logging.getLogger(__name__)

T = TypeVar('T')

class AIService:
    _instance = None
    _client = None

    def __new__(cls):
        """Implement singleton pattern to reuse the Gemini client."""
        if cls._instance is None:
            cls._instance = super(AIService, cls).__new__(cls)
        return cls._instance

    @property
    def is_ready(self) -> bool:
        """Returns True if the Gemini client is initialized and ready."""
        return self._client is not None

    def __init__(self):
        """Initializes the Gemini client using the new google-genai SDK."""
        # Ensure initialization only happens once
        if self._client is not None:
            return

        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY is not set. AI features will not function.")
            return

        try:
            # Initialize the new SDK client
            self._client = genai.Client(api_key=api_key)
            self.model_name = "gemini-2.5-flash"
            logger.info(f"AIService: Gemini client initialized successfully with model {self.model_name}.")
        except Exception as e:
            logger.error(f"AIService: Failed to initialize Gemini client: {e}")
            raise RuntimeError(f"AI Service initialization failed: {str(e)}")

    def _strip_markdown(self, text: str) -> str:
        """Strips markdown code blocks from the response text if present."""
        pattern = r"```(?:json)?\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    async def generate_text_response(self, prompt: str, temperature: float = 0.7) -> str:
        """Generates a plain text response from Gemini."""
        if not self._client:
            raise RuntimeError("Gemini client is not initialized.")

        try:
            logger.info("Generating text response...")
            config = types.GenerateContentConfig(temperature=temperature)
            # Using the async client (aio) for better performance in FastAPI
            response = await self._client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            
            if not response or not response.text:
                logger.warning("Gemini returned an empty text response.")
                return ""
                
            return response.text
        except Exception as e:
            logger.exception(f"Error in generate_text_response: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((json.JSONDecodeError, ValueError)),
        reraise=True
    )
    async def generate_json_response(
        self, 
        prompt: str, 
        response_schema: Optional[Union[Type[T], dict]] = None,
        temperature: float = 0.2
    ) -> Union[dict, T]:
        """
        Generates a structured JSON response.
        Includes markdown stripping, robust parsing, and retry logic.
        """
        if not self._client:
            raise RuntimeError("Gemini client is not initialized.")

        try:
            logger.info("Generating JSON response...")
            config = types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
                response_schema=response_schema if response_schema else None
            )

            response = await self._client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            if not response or not response.text:
                raise ValueError("Received empty response from Gemini.")

            cleaned_text = self._strip_markdown(response.text)
            
            if not cleaned_text:
                raise ValueError("Response text was empty after stripping markdown.")

            if response_schema and hasattr(response_schema, 'model_validate_json'):
                # Handle Pydantic model validation
                return response_schema.model_validate_json(cleaned_text)
            else:
                # Handle raw dict parsing
                return json.loads(cleaned_text)

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"JSON Parsing Error: {str(e)}. Response text: {response.text if 'response' in locals() else 'N/A'}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in generate_json_response: {str(e)}")
            raise

    # Existing MCP Tool Implementations (Refactored to use helpers)
    
    async def detect_pattern(self, problem: dict, code: str) -> PatternDetectionResponse:
        """Detects the most likely DSA pattern used or needed in the code."""
        prompt = f"""
        You are an expert Data Structures and Algorithms mentor. 
        Analyze the student's code for the given problem. Focus heavily on Arrays, Sliding Window, and Two Pointers.
        
        Problem: {json.dumps(problem)}
        Student Code:
        ```
        {code}
        ```
        
        Analyze whether the approach is brute force or optimized. Explain WHY the pattern fits the problem.
        Focus on pattern reasoning and invariant-related insights.
        Do NOT provide the complete solution.
        """
        try:
            return await self.generate_json_response(prompt, PatternDetectionResponse)
        except Exception as e:
            logger.error(f"Error in detect_pattern tool: {str(e)}")
            raise

    async def estimate_complexity(self, code: str) -> ComplexityEstimationResponse:
        """Estimates time and space complexity of the student's code."""
        prompt = f"""
        You are an expert Data Structures and Algorithms mentor.
        Analyze the time and space complexity of the following code.
        
        Student Code:
        ```
        {code}
        ```
        
        Focus on algorithmic reasoning. Explain what operations dominate complexity and WHY.
        If optimizations are possible, explain WHY optimization reduces complexity.
        Educational explanations only. Do NOT provide rewritten optimized code.
        """
        try:
            return await self.generate_json_response(prompt, ComplexityEstimationResponse)
        except Exception as e:
            logger.error(f"Error in estimate_complexity tool: {str(e)}")
            raise

    async def generate_hints(self, problem: dict, code: str) -> LayeredHintResponse:
        """Generates layered hints for the student's code."""
        prompt = f"""
        You are an expert Data Structures and Algorithms mentor.
        Your goal is to guide the student towards an optimal solution for the problem below, 
        based on their current code. Focus on Arrays, Sliding Window, and Two Pointers.
        
        Problem: {json.dumps(problem)}
        Student Code:
        ```
        {code}
        ```
        
        Provide layered hints. Progressively guide the student.
        IMPORTANT RULES:
        - NEVER give away the full solution or exact code.
        - Focus on helping students think independently.
        - Mention invariant maintenance when relevant.
        - Be encouraging but educational.
        """
        try:
            return await self.generate_json_response(prompt, LayeredHintResponse)
        except Exception as e:
            logger.error(f"Error in generate_hints tool: {str(e)}")
            raise

    async def generate_visual_steps(self, problem: dict, code: str) -> VisualizeResponse:
        """Generates structured execution steps for algorithm visualization."""
        prompt = f"""
        You are an expert Data Structures and Algorithms mentor.
        Your goal is to generate structured algorithm execution steps for the problem below, 
        based on the provided code. These steps will be used for a frontend animation.
        
        FOCUS: Arrays, Sliding Window, and Two Pointers.
        Problem: {json.dumps(problem)}
        Student Code:
        ```
        {code}
        ```
        
        RULES:
        - Breakdown the algorithm execution into small, clear steps.
        - Each step should represent a single state transition (e.g., moving a pointer, updating an answer).
        - Use ONLY these actions: expand, shrink, move_left, move_right, update_answer, remove_duplicate, restore_validity.
        - Explain WHY each transition occurs and how it relates to the invariant.
        - Be educationally descriptive but concise.
        - Ensure `window_state` reflects the content of the current subarray or window.
        
        Respond strictly with JSON matching the VisualizeResponse schema.
        """
        try:
            return await self.generate_json_response(prompt, VisualizeResponse)
        except Exception as e:
            logger.error(f"Error in generate_visual_steps tool: {str(e)}")
            raise
