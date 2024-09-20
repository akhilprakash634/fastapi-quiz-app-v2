from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any
from datetime import datetime
from bson import ObjectId
import random
from pydantic_core import core_schema

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

class QuizQuestion(BaseModel):
    id: str
    category: str
    difficulty: int
    question: str
    correct_answer: str
    incorrect_answers: List[str]

    def get_all_options(self) -> List[str]:
        options = self.incorrect_answers + [self.correct_answer]
        random.shuffle(options)
        return options

    def get_correct_option_index(self, shuffled_options: List[str]) -> int:
        return shuffled_options.index(self.correct_answer)

class FormattedQuizQuestion(BaseModel):
    id: str
    category: str
    difficulty: int
    question: str
    options: List[str]
    correct_option_index: int

class QuizSession(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    questions: List[FormattedQuizQuestion]
    start_time: datetime
    end_time: Optional[datetime] = None
    score: Optional[int] = None

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class QuizSessionCreate(BaseModel):
    category: Optional[str] = None
    difficulty: Optional[int] = None
    num_questions: int = 10

class UserAnswer(BaseModel):
    question_id: str
    selected_option_index: int

class QuizSubmission(BaseModel):
    session_id: str
    answers: List[UserAnswer]

class QuizResult(BaseModel):
    session_id: PyObjectId
    user_id: str
    score: int
    total_questions: int
    start_time: datetime
    end_time: datetime
    category: Optional[str] = None
    difficulty: Optional[int] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )