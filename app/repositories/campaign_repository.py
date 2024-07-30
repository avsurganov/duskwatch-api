import uuid
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.campaign_model import CreateCampaignRequest
from app.schemas.campaigns_schema import Campaign


class CampaignRepository:
    @staticmethod
    def create_campaign(db: Session, user_id: int, campaign: CreateCampaignRequest) -> Optional[Campaign]:
        try:
            db_campaign = Campaign(
                name=campaign.name,
                description=campaign.description,
                game_master_id=user_id
            )
            db.add(db_campaign)
            db.commit()
            db.refresh(db_campaign)
            return db_campaign
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating campaign: {str(e)}")
            return None

    @staticmethod
    def get_campaign(db: Session, campaign_id: uuid) -> Optional[Campaign]:
        try:
            return db.query(Campaign).filter(Campaign.id == campaign_id).first()
        except SQLAlchemyError as e:
            print(f"Error retrieving user by ID: {e}")
            return None

    @staticmethod
    def delete_campaign(db: Session, campaign: Campaign) -> bool:
        try:
            db.delete(campaign)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            return False


campaign_repository = CampaignRepository()
