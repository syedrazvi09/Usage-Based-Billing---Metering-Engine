from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class EventCreate(BaseModel):
    event_type : str
    quantity : Decimal
    idempotency_key : str
    occurred_at : Optional[datetime] = None
    