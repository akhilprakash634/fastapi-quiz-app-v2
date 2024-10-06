import logging
from fastapi import FastAPI
from app.core.config import settings
from app.database.mongodb import connect_to_mongo, close_mongo_connection, get_database
from app.routers import categories, auth, questions, quiz, leaderboard, invites
from app.services.question_service import QuestionService




app = FastAPI(title=settings.APP_NAME)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(categories.router)
app.include_router(questions.router)
app.include_router(auth.router)
app.include_router(quiz.router)
app.include_router(leaderboard.router)
app.include_router(invites.router)

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.APP_NAME} API"}


@app.on_event("startup")
async def startup_event():
    QuestionService.load_questions("./app/questions/questions.json")

    try:
        db = await get_database()
        await db.command("ping")
        logging.info("Successfully connected to MongoDB")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")
