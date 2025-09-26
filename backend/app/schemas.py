from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, validator


class AudienceBase(BaseModel):
    demographics: str = Field(..., max_length=255)
    interests: str | None = None


class AudienceCreate(AudienceBase):
    pass


class AudienceRead(AudienceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AdSetBase(BaseModel):
    name: str = Field(..., max_length=255)
    budget: int = Field(..., ge=0)
    audience: AudienceCreate


class AdSetCreate(AdSetBase):
    pass


class AdSetRead(AdSetBase):
    id: int
    created_at: datetime
    updated_at: datetime
    audience: AudienceRead

    class Config:
        orm_mode = True


class CampaignBase(BaseModel):
    name: str = Field(..., max_length=255)
    objective: str = Field(..., max_length=100)
    status: str = Field("draft", max_length=50)

    @validator("status")
    def validate_status(cls, value: str) -> str:
        allowed = {"draft", "active", "paused", "completed"}
        if value not in allowed:
            raise ValueError(f"Status must be one of: {', '.join(sorted(allowed))}")
        return value


class CampaignCreate(CampaignBase):
    ad_sets: list[AdSetCreate]


class CampaignRead(CampaignBase):
    id: int
    created_at: datetime
    updated_at: datetime
    ad_sets: list[AdSetRead]

    class Config:
        orm_mode = True
