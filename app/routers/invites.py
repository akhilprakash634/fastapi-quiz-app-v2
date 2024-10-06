from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter(prefix="/invites", tags=["invites"])

@router.get("/generate")
async def generate_invite_link(current_user: User = Depends(get_current_user)):
    invite_link = await UserService.generate_invite_link(current_user.id)
    if not invite_link:
        raise HTTPException(status_code=404, detail="User not found")
    return {"invite_link": invite_link}