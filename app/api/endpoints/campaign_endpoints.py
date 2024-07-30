from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.campaign_model import Campaign, CreateCampaignRequest
from app.models.common.common_model import ApiResponse, OperationResult
from app.models.common.common_responses import common_responses
from app.models.user_model import User
from app.repositories.campaign_repository import campaign_repository
from app.utils.jwt_utils import get_current_user

router = APIRouter()


@router.post("/", response_model=ApiResponse[Campaign], responses=common_responses)
def create_campaign(campaign_in: CreateCampaignRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    campaign = campaign_repository.create_campaign(db, current_user.id, campaign_in)
    if campaign is None:
        raise HTTPException(status_code=500)
    return ApiResponse(data=campaign)


@router.get("/{campaign_id}", response_model=ApiResponse[Campaign], responses=common_responses)
def get_campaign(campaign_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    campaign = campaign_repository.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if current_user.id != campaign.game_master_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this campaign")
    return ApiResponse(data=campaign)


@router.delete("/{campaign_id}", response_model=ApiResponse[OperationResult], responses=common_responses)
def delete_campaign(campaign_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    campaign = campaign_repository.get_campaign(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if current_user.id != campaign.game_master_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this campaign")
    success = campaign_repository.delete_campaign(db, campaign)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete campaign")
    return ApiResponse(data=OperationResult(success=True))

