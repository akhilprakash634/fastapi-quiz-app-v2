import logging
from app.database.mongodb import get_database
from app.models.leaderboard import GlobalLeaderboardResponse, LeaderboardEntry, LeaderboardResponse
from bson import ObjectId
from datetime import datetime, timedelta

class LeaderboardService:
    @staticmethod
    async def update_leaderboard(user_id: str, username: str, category: str, score: int):
        logging.info(f"Updating leaderboard: user_id={user_id}, username={username}, category={category}, score={score}")
        db = await get_database()
        leaderboard = db.leaderboards
        
        existing_entry = await leaderboard.find_one({"user_id": user_id, "category": category})
        
        if existing_entry and existing_entry["score"] < score:
            logging.info(f"Updating existing entry for user {user_id} in category {category}")
            await leaderboard.update_one(
                {"_id": existing_entry["_id"]},
                {"$set": {"score": score, "timestamp": datetime.utcnow()}}
            )
        elif not existing_entry:
            logging.info(f"Creating new entry for user {user_id} in category {category}")
            await leaderboard.insert_one({
                "user_id": user_id,
                "username": username,
                "category": category,
                "score": score,
                "timestamp": datetime.utcnow()
            })
        else:
            logging.info(f"No update needed for user {user_id} in category {category}")

    @staticmethod
    async def get_leaderboard(category: str, limit: int = 10) -> LeaderboardResponse:
        logging.info(f"Fetching leaderboard for category: {category}, limit: {limit}")
        db = await get_database()
        leaderboard = db.leaderboards
        
        entries = await leaderboard.find({"category": category}) \
                                   .sort("score", -1) \
                                   .limit(limit) \
                                   .to_list(length=limit)
        
        logging.info(f"Found {len(entries)} entries for category {category}")
        return LeaderboardResponse(
            category=category,
            entries=[LeaderboardEntry(**{**entry, '_id': str(entry['_id'])}) for entry in entries]
        )
    
    @staticmethod
    async def get_global_leaderboard(time_period: str = "all", limit: int = 10) -> GlobalLeaderboardResponse:
        logging.info(f"Fetching global leaderboard for time period: {time_period}, limit: {limit}")
        db = await get_database()
        leaderboard = db.leaderboards

        # Define the time range based on the time_period
        now = datetime.utcnow()
        if time_period == "daily":
            start_time = now - timedelta(days=1)
        elif time_period == "weekly":
            start_time = now - timedelta(weeks=1)
        elif time_period == "monthly":
            start_time = now - timedelta(days=30)
        else:  # "all" time
            start_time = None

        # Prepare the aggregation pipeline
        pipeline = []
        if start_time:
            pipeline.append({"$match": {"timestamp": {"$gte": start_time}}})

        pipeline.extend([
            {"$group": {
                "_id": {"user_id": "$user_id", "category": "$category"},
                "username": {"$first": "$username"},
                "score": {"$max": "$score"},
                "timestamp": {"$max": "$timestamp"}
            }},
            {"$sort": {"score": -1}},
            {"$group": {
                "_id": "$_id.category",
                "entries": {"$push": {
                    "_id": {"$toString": "$_id.user_id"},  # Use user_id as _id
                    "user_id": "$_id.user_id",
                    "username": "$username",
                    "score": "$score",
                    "timestamp": "$timestamp"
                }}
            }},
            {"$project": {
                "category": "$_id",
                "entries": {"$slice": ["$entries", limit]}
            }}
        ])

        results = await leaderboard.aggregate(pipeline).to_list(length=None)

        # Transform the results into the desired format
        categories = []
        for result in results:
            category = result['category']
            entries = [LeaderboardEntry(**entry) for entry in result['entries']]
            categories.append(LeaderboardResponse(category=category, entries=entries))

        return GlobalLeaderboardResponse(time_period=time_period, categories=categories)