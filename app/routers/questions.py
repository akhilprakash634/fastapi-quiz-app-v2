from fastapi import APIRouter, Query, Path
from app.services.question_service import QuestionService
from typing import List, Dict

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/category/{category}")
async def get_questions_by_category(
    category: str = Path(..., description="The category of questions to retrieve"),
    limit: int = Query(10, ge=1, le=50, description="Number of questions to retrieve")
) -> List[Dict]:
    return QuestionService.get_questions_by_category(category, limit)

@router.get("/random")
async def get_random_questions(
    limit: int = Query(10, ge=1, le=50, description="Number of questions to retrieve")
) -> List[Dict]:
    return QuestionService.get_random_questions(limit)

@router.get("/difficulty/{difficulty}")
async def get_questions_by_difficulty(
    difficulty: int = Path(..., ge=1, le=5, description="Difficulty level of questions"),
    limit: int = Query(10, ge=1, le=50, description="Number of questions to retrieve")
) -> List[Dict]:
    return QuestionService.get_questions_by_difficulty(difficulty, limit)