from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PatternDetectionResponse(BaseModel):
    detected_pattern: str
    confidence: float
    reasoning: str
    signals: List[str]
    optimization_possible: bool
    recommended_pattern: str

class ComplexityEstimationResponse(BaseModel):
    time_complexity: str
    space_complexity: str
    reasoning: str
    performance_bottlenecks: List[str]
    optimization_opportunities: List[str]

class LayeredHintResponse(BaseModel):
    conceptual_hint: str
    data_structure_hint: str
    logic_hint: str
    common_mistake_warning: str
    invariant_hint: str

class AnalysisResponse(BaseModel):
    problem_id: str
    detected_pattern: str
    feedback: str

class VisualStep(BaseModel):
    step_number: int
    left_pointer: Optional[int] = None
    right_pointer: Optional[int] = None
    window_state: Any
    action: str
    explanation: str
    invariant_status: str

class VisualizeResponse(BaseModel):
    pattern: str
    invariant: str
    steps: List[VisualStep]

class SimilarQuestion(BaseModel):
    title: str
    url: str
    difficulty: str

class SimilarResponse(BaseModel):
    recommendations: List[SimilarQuestion]

class OrchestrationResponse(BaseModel):
    problem: ProblemDetail
    pattern_analysis: PatternDetectionResponse
    complexity_analysis: ComplexityEstimationResponse
    hints: LayeredHintResponse
    visualization: VisualizeResponse

class Example(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None

class ProblemDetail(BaseModel):
    title: str
    description: str
    constraints: List[str]
    examples: List[Example]
    difficulty: str
    topic_tags: List[str]
    url: str
