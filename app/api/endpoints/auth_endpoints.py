from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.deps import get_db
from app.models.common.common_model import ApiResponse
from app.models.common.common_responses import common_responses
from app.models.user_model import AuthUser, LoginRequest
from app.repositories.user_repository import user_repository
from app.utils.jwt_utils import create_access_token

router = APIRouter()


@router.post("/token", response_model=ApiResponse[AuthUser], responses=common_responses)
def login_for_access_token(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = user_repository.authenticate_user(db=db, email=login_request.email, password=login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user_id": str(user.id)})
    return ApiResponse(data=AuthUser(user_id=str(user.id), access_token=access_token))
