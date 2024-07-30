from fastapi import APIRouter
from app.api.endpoints import auth_endpoints as auth
from app.api.endpoints import user_endpoints as users
from app.api.endpoints import campaign_endpoints as campaigns

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
