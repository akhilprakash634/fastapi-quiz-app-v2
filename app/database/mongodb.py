from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None

db = MongoDB()

async def get_database() -> AsyncIOMotorClient:
    return db.client[settings.MONGO_DB_NAME]

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URL)
    print(f"Connected to MongoDB: {settings.MONGO_DB_NAME}")

async def close_mongo_connection():
    db.client.close()
    print("Closed MongoDB connection")