from fastapi import FastAPI, Depends, HTTPException, HHeader, Response
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Customer, RawEvent
from app.schemas import EventCreate


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

def event_to_dict(event : RawEvent, duplicate : bool) -> dict:
    return {
        "id" : event.id,
        "customer_id" : event.customer_id,
        "event_type" : event.event_type,
        "quantity" : str(event.quantity),
        "idempotency_key" : event.idempotency_key,
        "occured_at" : event.occurred_at.isoformat(),
        "ingested_at" : event.ingested_at.isoformat(),
        "duplicate" : duplicate,
    }


@app.post("/events", status_code=201)
def create_event(
    payload : EventCreate,
    response : Response,
    db : Session = Depends(get_db),
):
    occurred_at = payload.occurred_at or datetime.now(timezone.utc)

    new_event = RawEvent(
        event_type = payload.event_type,
        quantity = payload.quantity,
        idempotency_key = payload.idempotency_key,
        occurred_at = occurred_at,
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return event_to_dict(new_event, duplicate=False)