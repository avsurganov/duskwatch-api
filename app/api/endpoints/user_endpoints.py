from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.common.common_model import ApiResponse
from app.models.common.common_responses import common_responses
from app.utils.jwt_utils import create_access_token, get_current_user
from app.models.user_model import User, AuthUser, RegisterUserRequest
from app.repositories.user_repository import user_repository

router = APIRouter()


@router.post("/", response_model=ApiResponse[AuthUser], responses=common_responses)
def create_user(user_in: RegisterUserRequest, db: Session = Depends(get_db)):
    user = user_repository.create_user(db=db, user=user_in)
    if user is None:
        raise HTTPException(status_code=403, detail="Email already registered")
    access_token = create_access_token(data={"user_id": str(user.id)})
    return ApiResponse(data=AuthUser(user_id=str(user.id), access_token=access_token))


@router.get("/{user_id}", response_model=ApiResponse[User], responses=common_responses)
def read_user(user_id: int, current_user: User = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=404, detail="User not found")
    return ApiResponse(data=current_user)


@router.delete("/{user_id}", response_model=ApiResponse[User], responses=common_responses)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id is not current_user.id:
        raise HTTPException(status_code=404, detail="User not found")
    user_repository.delete_user(db=db, user_id=user_id)
    return ApiResponse(data=current_user)
