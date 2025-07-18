# backend/app/services/model_service.py
from app.utils.code_analyzer import CodeAnalyzer
from app.services.model_service import ModelService
from app.models.response_models import CodeFeedbackResponse, FeedbackCategory, CodeSuggestion
from datetime import datetime
import ollama
import json
import logging
from typing import Dict, Any, Optional
from app.models.request_models import CodeSubmissionRequest

logger = logging.getLogger(__name__)


class ModelService:
    def __init__(self):
        self.model_name = "codellama:7b"  # Will be updated to your fine-tuned model
        self.client = ollama.Client()
        self.is_initialized = False

    async def initialize(self):
        """Initialize the model service"""
        try:
            # Check if model is available
            models = self.client.list()
            available_models = [model['name'] for model in models['models']]

            if self.model_name not in available_models:
                logger.info(f"Pulling {self.model_name} model...")
                self.client.pull(self.model_name)

            # Test model with a simple prompt
            test_response = self.client.generate(
                model=self.model_name,
                prompt="Test prompt",
                options={'num_predict': 10}
            )

            self.is_initialized = True
            logger.info("Model service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise

    def is_ready(self) -> bool:
        """Check if model service is ready"""
        return self.is_initialized

    def create_feedback_prompt(self, request: CodeSubmissionRequest) -> str:
        """Create a structured prompt for code feedback generation"""

        base_prompt = f"""You are an expert programming instructor providing constructive feedback on student code.

**Student Code ({request.language}):**
```{request.language}
{request.code}
```

**Assignment Context:** {request.assignment_context or "General code review"}
**Student Level:** {request.student_level}
**Feedback Focus:** {request.feedback_type}

Please provide comprehensive feedback in the following JSON format:
{{
    "overall_score": <score from 0-100>,
    "feedback_categories": {{
        "correctness": "<feedback on code correctness>",
        "style": "<feedback on code style and formatting>",
        "efficiency": "<feedback on algorithm efficiency>",
        "best_practices": "<feedback on programming best practices>",
        "debugging": "<debugging suggestions if applicable>"
    }},
    "specific_suggestions": [
        {{
            "line_number": <line number or null>,
            "issue_type": "<type of issue>",
            "description": "<description of issue>",
            "suggestion": "<suggested improvement>",
            "severity": "<low/medium/high>"
        }}
    ],
    "corrected_code": "<improved version of code if applicable>",
    "summary": "<brief summary of key points>",
    "strengths": ["<strength1>", "<strength2>"],
    "areas_for_improvement": ["<area1>", "<area2>"]
}}

Focus on being constructive, educational, and encouraging. Provide specific, actionable feedback."""

        return base_prompt

    async def generate_feedback(self, request: CodeSubmissionRequest) -> Dict[str, Any]:
        """Generate feedback for the submitted code"""
        try:
            if not self.is_initialized:
                raise RuntimeError("Model service not initialized")

            prompt = self.create_feedback_prompt(request)

            # Generate response using Ollama
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.3,  # Lower temperature for more consistent feedback
                    'num_predict': 2000,  # Max tokens for response
                    'top_p': 0.9,
                    'repeat_penalty': 1.1
                }
            )

            # Extract and parse the response
            raw_response = response['response']

            # Try to extract JSON from the response
            feedback_json = self._extract_json_from_response(raw_response)

            if not feedback_json:
                # Fallback: create structured response from raw text
                feedback_json = self._create_fallback_response(
                    raw_response, request)

            return feedback_json

        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            raise

    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from model response"""
        try:
            # Look for JSON block in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)

            return None

        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON from model response")
            return None

    def _create_fallback_response(self, raw_response: str, request: CodeSubmissionRequest) -> Dict[str, Any]:
        """Create a fallback structured response when JSON parsing fails"""
        return {
            "overall_score": 75.0,  # Default score
            "feedback_categories": {
                "correctness": "Analysis provided in summary",
                "style": "Style feedback included in summary",
                "efficiency": "Efficiency notes in summary",
                "best_practices": "Best practices mentioned in summary",
                "debugging": None
            },
            "specific_suggestions": [
                {
                    "line_number": None,
                    "issue_type": "general",
                    "description": "Detailed analysis provided",
                    "suggestion": "See summary for specific recommendations",
                    "severity": "medium"
                }
            ],
            "corrected_code": None,
            "summary": raw_response[:500] + "..." if len(raw_response) > 500 else raw_response,
            "strengths": ["Code submitted for review"],
            "areas_for_improvement": ["See detailed feedback above"]
        }


# backend/app/services/feedback_service.py

logger = logging.getLogger(__name__)


class FeedbackService:
    def __init__(self, model_service: ModelService):
        self.model_service = model_service
        self.code_analyzer = CodeAnalyzer()

    async def generate_feedback(self, request: CodeSubmissionRequest) -> CodeFeedbackResponse:
        """Generate comprehensive feedback for submitted code"""
        try:
            # Get AI-generated feedback
            ai_feedback = await self.model_service.generate_feedback(request)

            # Enhance with static analysis if available
            static_analysis = self.code_analyzer.analyze_code(
                request.code, request.language)

            # Combine AI feedback with static analysis
            enhanced_feedback = self._enhance_feedback(
                ai_feedback, static_analysis)

            # Create response model
            response = CodeFeedbackResponse(
                overall_score=enhanced_feedback.get('overall_score', 75.0),
                feedback_categories=FeedbackCategory(
                    **enhanced_feedback.get('feedback_categories', {})),
                specific_suggestions=[
                    CodeSuggestion(**suggestion)
                    for suggestion in enhanced_feedback.get('specific_suggestions', [])
                ],
                corrected_code=enhanced_feedback.get('corrected_code'),
                summary=enhanced_feedback.get(
                    'summary', 'Feedback generated successfully'),
                strengths=enhanced_feedback.get('strengths', []),
                areas_for_improvement=enhanced_feedback.get(
                    'areas_for_improvement', []),
                generated_at=datetime.now()
            )

            return response

        except Exception as e:
            logger.error(f"Error in feedback generation: {e}")
            raise

    def _enhance_feedback(self, ai_feedback: dict, static_analysis: dict) -> dict:
        """Enhance AI feedback with static analysis results"""
        enhanced = ai_feedback.copy()

        # Add static analysis insights to suggestions
        if static_analysis.get('issues'):
            for issue in static_analysis['issues']:
                enhanced['specific_suggestions'].append({
                    'line_number': issue.get('line_number'),
                    'issue_type': 'static_analysis',
                    'description': issue.get('description', ''),
                    'suggestion': issue.get('suggestion', ''),
                    'severity': issue.get('severity', 'medium')
                })

        # Adjust overall score based on static analysis
        if static_analysis.get('score_adjustment'):
            current_score = enhanced.get('overall_score', 75.0)
            enhanced['overall_score'] = max(
                0, min(100, current_score + static_analysis['score_adjustment']))

        return enhanced
