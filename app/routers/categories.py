from fastapi import APIRouter, Depends
from app.services.question_service import QuestionService
from typing import List

from app.models.user import User
from app.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[str])
async def list_categories(
    current_user: User = Depends(get_current_user)
):
    return QuestionService.get_all_categories()