from fastapi import APIRouter,Depends,status
from utils.validation_models.disaster_zone import DisasterZoneDto,CreateDisasterZoneDto
from config.db import db_connection
from models.disaster_zones import DisasterZone

router=APIRouter()

from sqlalchemy import select
from sqlalchemy.orm import Session


@router.get("/zones")
def get_zones(db: Session = Depends(db_connection)):

    stmt = (
        select(DisasterZone)
        .order_by(DisasterZone.created_at.desc())
    )

    zones = db.scalars(stmt).all()

    return zones