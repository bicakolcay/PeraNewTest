from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Campaign(TimestampMixin, Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    objective: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft")

    ad_sets: Mapped[list[AdSet]] = relationship(
        "AdSet", back_populates="campaign", cascade="all, delete-orphan"
    )


class AdSet(TimestampMixin, Base):
    __tablename__ = "ad_sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    budget: Mapped[int] = mapped_column(Integer, nullable=False)

    campaign: Mapped[Campaign] = relationship("Campaign", back_populates="ad_sets")
    audience: Mapped[Audience] = relationship(
        "Audience", back_populates="ad_set", uselist=False, cascade="all, delete-orphan"
    )


class Audience(TimestampMixin, Base):
    __tablename__ = "audiences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ad_set_id: Mapped[int] = mapped_column(ForeignKey("ad_sets.id", ondelete="CASCADE"))
    demographics: Mapped[str] = mapped_column(String(255), nullable=False)
    interests: Mapped[str | None] = mapped_column(Text, nullable=True)

    ad_set: Mapped[AdSet] = relationship("AdSet", back_populates="audience")
