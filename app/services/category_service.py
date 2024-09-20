from app.models.category import CategoryModel
from app.database.mongodb import get_database
from bson import ObjectId

class CategoryService:
    @staticmethod
    async def create_category(category: CategoryModel) -> CategoryModel:
        db = await get_database()
        category_dict = category.to_mongo()
        result = await db.categories.insert_one(category_dict)
        created_category = await db.categories.find_one({"_id": result.inserted_id})
        return CategoryModel.from_mongo(created_category)

    @staticmethod
    async def get_category(category_id: str) -> CategoryModel:
        db = await get_database()
        category = await db.categories.find_one({"_id": ObjectId(category_id)})
        if category:
            return CategoryModel.from_mongo(category)
        return None

    @staticmethod
    async def list_categories():
        db = await get_database()
        categories = await db.categories.find().to_list(length=100)
        return [CategoryModel.from_mongo(category) for category in categories]