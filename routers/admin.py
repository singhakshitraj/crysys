from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.sos_requests import SOSRequest,SosStatus
from models.disaster_zones import DisasterZone
from utils.validation_models.disaster_zone import CreateDisasterZoneDto,UpdateDisasterZoneDto
from config.db import db_connection

router = APIRouter(
    prefix='/admin'
)

@router.put("/sos/{sos_id}/status")
def update_status(
    sos_id: int,
    status: SosStatus = Query(...),
    db: Session = Depends(db_connection),
):

    sos = db.get(SOSRequest, sos_id)

    if not sos:
        raise HTTPException(404, "No such SosRequest")

    sos.status = status

    db.commit()
    db.refresh(sos)

    return sos

@router.post("/zones", status_code=status.HTTP_201_CREATED)
def create_disaster_zone(
    req: CreateDisasterZoneDto,
    db: Session = Depends(db_connection),
):

    zone = DisasterZone(
        name=req.name,
        disaster_type=req.disaster_type,
        danger_level=req.danger_level,
        latitude=req.center_latitude,
        longitude=req.center_longitude,
        radius=req.radius,
    )

    db.add(zone)
    db.commit()
    db.refresh(zone)

    return {
        "status": "201",
        "data": zone,
    }

@router.delete("/zones/{zone_id}")
def delete_disaster_zone(
    zone_id: int,
    db: Session = Depends(db_connection),
):

    zone = db.get(DisasterZone, zone_id)

    if not zone:
        raise HTTPException(404, "Zone not found")

    name = zone.name

    db.delete(zone)
    db.commit()

    return {
        "message": "Deleted Successfully!",
        "name": name,
    }

@router.put("/zones/{zone_id}")
def update_disaster_zone(
    zone_id: int,
    data: UpdateDisasterZoneDto,
    db: Session = Depends(db_connection),
):

    zone = db.get(DisasterZone, zone_id)

    if not zone:
        raise HTTPException(404, "Zone not found")

    zone.name = data.name
    zone.disaster_type = data.disaster_type
    zone.danger_level = data.danger_level
    zone.latitude = data.latitude
    zone.longitude = data.longitude
    zone.radius = data.radius

    db.commit()
    db.refresh(zone)

    return {
        "message": "Updated Successfully!",
        "name": zone.name,
    }
