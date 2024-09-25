from pydantic import BaseModel, Field

class EvaluationCriterion(BaseModel):
    score: float = Field(..., ge=0, le=10, description="Score from 0 to 10")
    # comments: str = Field(..., description="Justification for the score")

class EvaluationModel(BaseModel):
    intel_technology: EvaluationCriterion
    theme_relevance: EvaluationCriterion
    innovation_creativity: EvaluationCriterion
    technical_feasibility: EvaluationCriterion
    sustainability_impact: EvaluationCriterion
    presentation_clarity: EvaluationCriterion
    scalability_viability: EvaluationCriterion
    
    # overall_score: float = Field(..., ge=0, le=100, description="Overall score out of 100")
    # strengths: list[str] = Field(..., min_items=1, description="List of project strengths")
    # weaknesses: list[str] = Field(..., min_items=1, description="List of project weaknesses")
    # improvement_suggestions: list[str] = Field(..., min_items=1, description="Suggestions for improvement")