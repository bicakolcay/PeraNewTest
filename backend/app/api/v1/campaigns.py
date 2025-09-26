from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ... import schemas
from ...db import SessionLocal
from ...services.campaigns import CampaignService

router = APIRouter()


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_service(session: Session = Depends(get_session)) -> CampaignService:
    return CampaignService(session)


@router.get("/", response_model=list[schemas.CampaignRead])
def list_campaigns(service: CampaignService = Depends(get_service)):
    return service.list_campaigns()


@router.post("/", response_model=schemas.CampaignRead, status_code=201)
def create_campaign(
    payload: schemas.CampaignCreate, service: CampaignService = Depends(get_service)
):
    return service.create_campaign(payload)
