from app.models.user import UserCreate, UserInDB, User
from app.core.security import get_password_hash, verify_password
from app.database.mongodb import get_database
from bson import ObjectId

class UserService:
    @staticmethod
    async def create_user(user: UserCreate):
        db = await get_database()
        existing_user = await db.users.find_one({"username": user.username})
        if existing_user:
            return None
        user_in_db = UserInDB(**user.dict(), hashed_password=get_password_hash(user.password))
        result = await db.users.insert_one(user_in_db.dict(exclude={"id"}))
        return User(id=str(result.inserted_id), **user.dict(exclude={"password"}))

    @staticmethod
    async def authenticate_user(username: str, password: str):
        db = await get_database()
        user = await db.users.find_one({"username": username})
        if not user or not verify_password(password, user["hashed_password"]):
            return None
        return User(id=str(user["_id"]), **{k: v for k, v in user.items() if k not in ["_id", "hashed_password"]})

    @staticmethod
    async def get_user_by_username(username: str):
        db = await get_database()
        user = await db.users.find_one({"username": username})
        if user:
            return User(id=str(user["_id"]), **{k: v for k, v in user.items() if k not in ["_id", "hashed_password"]})
        return None