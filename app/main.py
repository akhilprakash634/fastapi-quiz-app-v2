from fastapi import FastAPI
from app.core.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.routers import categories
from app.services.question_service import QuestionService
from app.routers import questions

app = FastAPI(title=settings.APP_NAME)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(categories.router)
app.include_router(questions.router)

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.APP_NAME} API"}

@app.on_event("startup")
async def startup_event():
    QuestionService.load_questions("./app/questions/questions.json")
