from datetime import datetime
import logging
from fastapi import APIRouter, Depends, HTTPException
from app.models.quiz_session import QuizSessionCreate, QuizSession, QuizSubmission
from app.services.question_service import QuestionService
from app.dependencies import get_current_user
from app.models.user import User
from bson import ObjectId

from app.database.mongodb import get_database

router = APIRouter(prefix="/quiz", tags=["quiz"])

@router.post("/start", response_model=QuizSession)
async def start_quiz(quiz_create: QuizSessionCreate, current_user: User = Depends(get_current_user)):
    return await QuestionService.create_quiz_session(current_user.id, quiz_create)

@router.post("/submit", response_model=QuizSession)
async def submit_quiz(submission: QuizSubmission, current_user: User = Depends(get_current_user)):
    try:
        return await QuestionService.submit_quiz(submission)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/session/{session_id}", response_model=QuizSession)
async def get_session(session_id: str):
    logging.info(f"Test endpoint: Attempting to retrieve session with ID: {session_id}")
    session = await QuestionService.get_quiz_session(session_id)
    print(session_id)
    if not session:
        logging.error(f"Test endpoint: Quiz session not found for ID: {session_id}")
        raise HTTPException(status_code=404, detail=f"Quiz session not found for ID: {session_id}")
    logging.info(f"Test endpoint: Session retrieved: {session}")
    return session

# @router.post("/test-session", response_model=str)
# async def create_test_session():
#     db = await get_database()
#     test_session = {
#         "user_id": "test_user",
#         "questions": [
#             {
#                 "id": "1",
#                 "category": "Test",
#                 "difficulty": 1,
#                 "question": "Test Question",
#                 "options": ["A", "B", "C", "D"],
#                 "correct_option_index": 0
#             }
#         ],
#         "start_time": datetime.utcnow(),
#         "end_time": None,
#         "score": None
#     }
#     result = await db.quiz_sessions.insert_one(test_session)
#     session_id = str(result.inserted_id)
#     print(f"Inserted test session with ID: {session_id}")
#     return session_id

# @router.get("/test-session/{session_id}", response_model=QuizSession)
# async def get_test_session(session_id: str):
#     print(f"Attempting to retrieve test session with ID: {session_id}")
#     session = await QuestionService.get_quiz_session(session_id)
#     if not session:
#         print(f"Session not found for ID: {session_id}")
#         raise HTTPException(status_code=404, detail="Session not found")
#     print(f"Retrieved session: {session}")
#     return session