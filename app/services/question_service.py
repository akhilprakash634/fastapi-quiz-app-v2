import json
from typing import List, Dict
import random

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
    def get_questions_by_category(cls, category: str, limit: int = 10) -> List[Dict]:
        category_questions = [q for q in cls._questions if q['category'].lower() == category.lower()]
        return random.sample(category_questions, min(limit, len(category_questions)))

    @classmethod
    def get_random_questions(cls, limit: int = 10) -> List[Dict]:
        return random.sample(cls._questions, min(limit, len(cls._questions)))

    @classmethod
    def get_questions_by_difficulty(cls, difficulty: int, limit: int = 10) -> List[Dict]:
        difficulty_questions = [q for q in cls._questions if q['difficulty'] == difficulty]
        return random.sample(difficulty_questions, min(limit, len(difficulty_questions)))