from fastapi import APIRouter
from app.services.question_service import QuestionService
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[str])
async def list_categories():
    return QuestionService.get_all_categories()