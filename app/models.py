from sqlalchemy import (
    Column, Integer, String, DateTime, Numeric, JSON,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.sql import func

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RawEvent(Base):
    __tablename__ = "raw_events"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    event_type = Column(String, nullable=False)
    quantity = Column(Numeric, nullable=False)
    idempotency_key = Column(String, nullable=False)
    occurred_at = Column(DateTime(timezone=True), nullable=False)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("customer_id", "idempotency_key", name="uq_customer_idempotency_key"),
    )


class PricingPlan(Base):
    __tablename__ = "pricing_plans"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tiers = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())