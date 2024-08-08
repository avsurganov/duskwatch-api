from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateCampaignRequest(BaseModel):
    name: str
    description: str


class CampaignBase(BaseModel):
    id: UUID
    name: str
    description: str


class CampaignInDBBase(CampaignBase):
    game_master_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Campaign(CampaignInDBBase):
    pass
