import logging
from typing import Optional
from fastapi import APIRouter, Query
from app.services.leaderboard_service import LeaderboardService
from app.models.leaderboard import GlobalLeaderboardResponse, LeaderboardResponse

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/global", response_model=GlobalLeaderboardResponse)
async def get_global_leaderboard(
    time_period: Optional[str] = Query("all", enum=["daily", "weekly", "monthly", "all"]),
    limit: int = Query(10, ge=1, le=100)
):
    return await LeaderboardService.get_global_leaderboard(time_period, limit)

@router.get("/{category}", response_model=LeaderboardResponse)
async def get_leaderboard(category: str, limit: int = Query(10, ge=1, le=100)):
    logging.info(f"Fetching leaderboard for category: {category}, limit: {limit}")
    leaderboard = await LeaderboardService.get_leaderboard(category, limit)
    logging.info(f"Leaderboard fetched: {leaderboard}")
    return leaderboard