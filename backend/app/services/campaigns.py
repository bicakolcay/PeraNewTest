from __future__ import annotations

from typing import Iterable

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import schemas
from ..models import AdSet, Audience, Campaign


class CampaignService:
    """Business logic for campaign operations."""

    def __init__(self, session: Session):
        self.session = session

    def list_campaigns(self) -> Iterable[Campaign]:
        statement = select(Campaign).order_by(Campaign.created_at.desc())
        return self.session.scalars(statement).unique().all()

    def create_campaign(self, payload: schemas.CampaignCreate) -> Campaign:
        if not payload.ad_sets:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campaign must contain at least one ad set.",
            )

        campaign = Campaign(name=payload.name, objective=payload.objective, status=payload.status)

        for ad_set_data in payload.ad_sets:
            if ad_set_data.budget <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ad set budget must be greater than zero.",
                )

            ad_set = AdSet(name=ad_set_data.name, budget=ad_set_data.budget)
            audience_data = ad_set_data.audience
            audience = Audience(
                demographics=audience_data.demographics,
                interests=audience_data.interests,
            )
            ad_set.audience = audience
            campaign.ad_sets.append(ad_set)

        self.session.add(campaign)

        try:
            self.session.flush()
        except IntegrityError as exc:  # pragma: no cover - defensive
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Campaign with this name already exists.",
            ) from exc

        return campaign
