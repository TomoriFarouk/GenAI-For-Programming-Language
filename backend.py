# backend/requirements.txt
import logging
from app.services.feedback_service import FeedbackService
from app.services.model_service import ModelService
from app.models.response_models import CodeFeedbackResponse
from app.models.request_models import CodeSubmissionRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
fastapi == 0.104.1
uvicorn == 0.24.0
pydantic == 2.5.0
python-multipart == 0.0.6
ollama == 0.1.7
transformers == 4.36.0
torch == 2.1.0
numpy == 1.24.3
requests == 2.31.0
python-dotenv == 1.0.0

# backend/app/models/request_models.py


class ProgrammingLanguage(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"


class FeedbackType(str, Enum):
    GENERAL = "general"
    DEBUGGING = "debugging"
    STYLE = "style"
    ALGORITHM = "algorithm"
    BEST_PRACTICES = "best_practices"


class CodeSubmissionRequest(BaseModel):
    code: str = Field(..., description="The student's code submission")
    language: ProgrammingLanguage = Field(...,
                                          description="Programming language")
    assignment_context: Optional[str] = Field(
        None, description="Assignment description or context")
    feedback_type: FeedbackType = Field(
        FeedbackType.GENERAL, description="Type of feedback requested")
    student_level: Optional[str] = Field(
        "beginner", description="Student skill level")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
                "language": "python",
                "assignment_context": "Write a recursive function to calculate factorial",
                "feedback_type": "general",
                "student_level": "beginner"
            }
        }


# backend/app/models/response_models.py


class FeedbackCategory(BaseModel):
    correctness: Optional[str] = Field(
        None, description="Correctness feedback")
    style: Optional[str] = Field(None, description="Code style feedback")
    efficiency: Optional[str] = Field(
        None, description="Algorithm efficiency feedback")
    best_practices: Optional[str] = Field(
        None, description="Best practices feedback")
    debugging: Optional[str] = Field(None, description="Debugging suggestions")


class CodeSuggestion(BaseModel):
    line_number: Optional[int] = Field(
        None, description="Line number for suggestion")
    issue_type: str = Field(..., description="Type of issue identified")
    description: str = Field(..., description="Description of the issue")
    suggestion: str = Field(..., description="Suggested improvement")
    severity: str = Field(..., description="Severity level: low, medium, high")


class CodeFeedbackResponse(BaseModel):
    overall_score: float = Field(..., ge=0, le=100,
                                 description="Overall code quality score")
    feedback_categories: FeedbackCategory = Field(
        ..., description="Categorized feedback")
    specific_suggestions: List[CodeSuggestion] = Field(
        default=[], description="Specific code suggestions")
    corrected_code: Optional[str] = Field(
        None, description="Suggested code improvements")
    summary: str = Field(..., description="Summary of key points")
    strengths: List[str] = Field(
        default=[], description="Code strengths identified")
    areas_for_improvement: List[str] = Field(
        default=[], description="Areas needing improvement")
    generated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "overall_score": 85.0,
                "feedback_categories": {
                    "correctness": "The function correctly implements factorial calculation",
                    "style": "Code follows Python naming conventions",
                    "efficiency": "Recursive approach is clear but could be optimized"
                },
                "specific_suggestions": [
                    {
                        "line_number": 3,
                        "issue_type": "optimization",
                        "description": "Base case could include n == 1",
                        "suggestion": "Consider adding n == 1 case for slight optimization",
                        "severity": "low"
                    }
                ],
                "summary": "Well-structured recursive function with room for minor optimizations",
                "strengths": ["Clear logic", "Proper base case"],
                "areas_for_improvement": ["Add input validation", "Consider iterative approach"]
            }
        }


# backend/app/main.py

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Programming Assessment AI",
    description="AI-powered programming assignment feedback system",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
model_service = ModelService()
feedback_service = FeedbackService(model_service)


@app.on_event("startup")
async def startup_event():
    """Initialize model on startup"""
    try:
        await model_service.initialize()
        logger.info("Model service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize model service: {e}")


@app.get("/")
async def root():
    return {"message": "Programming Assessment AI API", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model_service.is_ready(),
        "timestamp": datetime.now()
    }


@app.post("/analyze-code", response_model=CodeFeedbackResponse)
async def analyze_code(request: CodeSubmissionRequest):
    """Main endpoint for code analysis and feedback generation"""
    try:
        logger.info(f"Analyzing {request.language} code submission")

        # Generate feedback using the model service
        feedback = await feedback_service.generate_feedback(request)

        logger.info("Feedback generated successfully")
        return feedback

    except Exception as e:
        logger.error(f"Error analyzing code: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze code: {str(e)}")


@app.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": ["python", "java", "javascript"],
        "feedback_types": ["general", "debugging", "style", "algorithm", "best_practices"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
