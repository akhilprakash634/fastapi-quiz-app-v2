import json
import logging
import random
from typing import List, Dict
from bson import ObjectId
from datetime import datetime
from app.models.quiz_session import FormattedQuizQuestion, QuizSession, QuizSessionCreate, QuizQuestion, QuizSubmission, UserAnswer
from app.database.mongodb import get_database

class QuestionService:
    _questions: List[Dict] = []

    @classmethod
    def load_questions(cls, file_path: str):
        with open(file_path, 'r') as file:
            cls._questions = json.load(file)
        print(f"Loaded {len(cls._questions)} questions")

    @classmethod
    def get_all_categories(cls) -> List[str]:
        return list(set(question['category'] for question in cls._questions))

    @classmethod
    def get_questions_by_category(cls, category: str, num_questions: int) -> List[Dict]:
        category_questions = [q for q in cls._questions if q['category'].lower() == category.lower()]
        return random.sample(category_questions, min(num_questions, len(category_questions)))

    @classmethod
    def get_questions_by_difficulty(cls, difficulty: int, num_questions: int) -> List[Dict]:
        difficulty_questions = [q for q in cls._questions if q['difficulty'] == difficulty]
        return random.sample(difficulty_questions, min(num_questions, len(difficulty_questions)))

    @classmethod
    def get_random_questions(cls, num_questions: int) -> List[Dict]:
        return random.sample(cls._questions, min(num_questions, len(cls._questions)))

    @classmethod
    def get_questions(cls, quiz_create: QuizSessionCreate) -> List[Dict]:
        if quiz_create.category:
            return cls.get_questions_by_category(quiz_create.category, quiz_create.num_questions)
        elif quiz_create.difficulty:
            return cls.get_questions_by_difficulty(quiz_create.difficulty, quiz_create.num_questions)
        else:
            return cls.get_random_questions(quiz_create.num_questions)

    
    @classmethod
    def format_question(cls, question: dict) -> FormattedQuizQuestion:
        quiz_question = QuizQuestion(**question)
        options = quiz_question.get_all_options()
        correct_option_index = quiz_question.get_correct_option_index(options)
        return FormattedQuizQuestion(
            id=quiz_question.id,
            category=quiz_question.category,
            difficulty=quiz_question.difficulty,
            question=quiz_question.question,
            options=options,
            correct_option_index=correct_option_index
        )

    @classmethod
    async def create_quiz_session(cls, user_id: str, quiz_create: QuizSessionCreate) -> QuizSession:
        questions = cls.get_questions(quiz_create)
        formatted_questions = [cls.format_question(q) for q in questions]
        session_id = ObjectId()
        session_data = {
            "_id": session_id,
            "user_id": user_id,
            "questions": [q.dict() for q in formatted_questions],
            "start_time": datetime.utcnow(),
            "end_time": None,
            "score": None
        }
        db = await get_database()
        await db.quiz_sessions.insert_one(session_data)
        return QuizSession(
            id=str(session_id),
            user_id=user_id,
            questions=formatted_questions,  # Use FormattedQuizQuestion objects directly
            start_time=session_data["start_time"],
            end_time=None,
            score=None
        )

    @classmethod
    async def get_quiz_session(cls, session_id: str) -> QuizSession:
        print(f"Attempting to retrieve quiz session with ID: {session_id}")
        db = await get_database()
        try:
            object_id = ObjectId(session_id)
            session_data = await db.quiz_sessions.find_one({"_id": object_id})
            print(f"Retrieved session data: {session_data}")
            if session_data:
                # Convert dictionary questions back to FormattedQuizQuestion objects
                formatted_questions = [FormattedQuizQuestion(**q) for q in session_data['questions']]
                return QuizSession(
                    id=str(session_data['_id']),
                    user_id=session_data['user_id'],
                    questions=formatted_questions,
                    start_time=session_data['start_time'],
                    end_time=session_data.get('end_time'),
                    score=session_data.get('score')
                )
            else:
                print(f"No quiz session found with ID: {session_id}")
                return None
        except Exception as e:
            print(f"Error retrieving quiz session: {str(e)}")
            return None

    @classmethod
    async def submit_quiz(cls, submission: QuizSubmission) -> QuizSession:
        db = await get_database()
        session = await cls.get_quiz_session(submission.session_id)
        
        if not session:
            raise ValueError("Invalid session ID")

        score = 0
        for answer in submission.answers:
            question = next((q for q in session.questions if q.id == answer.question_id), None)
            if question and answer.selected_option_index == question.correct_option_index:
                score += 1

        session.end_time = datetime.utcnow()
        session.score = score

        await db.quiz_sessions.update_one(
            {"_id": ObjectId(session.id)},
            {"$set": {"end_time": session.end_time, "score": session.score}}
        )

        return session

    @classmethod
    async def get_user_quiz_history(cls, user_id: str) -> List[QuizSession]:
        db = await get_database()
        sessions_data = await db.quiz_sessions.find({"user_id": user_id}).to_list(length=100)
        return [QuizSession(**session_data) for session_data in sessions_data]

    # You might want to add more methods here as needed for your application