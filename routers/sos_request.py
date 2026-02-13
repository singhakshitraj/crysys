from sqlalchemy.orm import Session
from models.sos_requests import SOSRequest
from models.enums import SosStatus
from fastapi import HTTPException
from datetime import datetime
from fastapi import APIRouter,Depends,Query
from config.db import db_connection
from utils.current_user import get_current_user
from models.user import User
from sqlalchemy import select
router = APIRouter(
    prefix='/sos'
)

def create_sos_request(data, user_id, db: Session):
    sos = SOSRequest(
        user_id=user_id,
        latitude=data.latitude,
        longitude=data.longitude,
        message=data.message,
        disaster_type=data.disaster_type,
        status=SosStatus.PENDING.value
    )

    db.add(sos)
    db.commit()
    db.refresh(sos)

    return sos

def update_pending_sos_request(data, sos_id, user_id, db: Session):

    sos = db.query(SOSRequest).filter(
        SOSRequest.id == sos_id
    ).first()

    if not sos:
        raise HTTPException(404, "No such SOSRequest")

    if sos.status != SosStatus.PENDING.value:
        raise HTTPException(400, "Only pending requests can be updated")

    if sos.user_id != user_id:
        raise HTTPException(403, "Not allowed")

    sos.latitude = data.latitude
    sos.longitude = data.longitude
    sos.message = data.message
    sos.disaster_type = data.disaster_type
    sos.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(sos)

    return sos

def get_user_sos_requests(user_id, db: Session):

    return db.query(SOSRequest).filter(
        SOSRequest.user_id == user_id
    ).all()

def delete_pending_sos_request(sos_id, user, db: Session):

    sos = db.query(SOSRequest).filter(
        SOSRequest.id == sos_id
    ).first()

    if not sos:
        raise HTTPException(404, "No such SOSRequest")

    if sos.status != SosStatus.PENDING.value:
        raise HTTPException(400, "Only pending requests can be deleted")

    if sos.user_id != user["id"]:
        raise HTTPException(403, "Not allowed")

    db.delete(sos)
    db.commit()

    return {"message": f"Request deleted successfully with id {sos_id}"}

from sqlalchemy.orm import Session
from utils.validation_models.sos_request import CreateSosRequest

@router.post("/", status_code=201)
def create_sos(
    data: CreateSosRequest,
    user=Depends(get_current_user),
    db: Session = Depends(db_connection)
):
    return create_sos_request(data, user, db)

@router.put("/{sos_id}")
def update_sos(
    sos_id: int,
    data: CreateSosRequest,
    user=Depends(get_current_user),
    db: Session = Depends(db_connection)
):
    return update_pending_sos_request(data, sos_id, user, db)

@router.get("/")
def get_my_sos(
    user=Depends(get_current_user),
    db: Session = Depends(db_connection)
):
    return get_user_sos_requests(user, db)

@router.delete("/{sos_id}")
def delete_sos(
    sos_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(db_connection)
):
    return delete_pending_sos_request(sos_id, user, db)

from sqlalchemy.orm import Session
from models.sos_requests import SOSRequest


def get_filtered_requests(
    status: str | None,
    zone_id: int | None,
    db: Session
):
    query = db.query(SOSRequest)

    if status is not None:
        query = query.filter(SOSRequest.status == status)

    if zone_id is not None:
        query = query.filter(SOSRequest.zone_id == zone_id)

    return query.order_by(SOSRequest.created_at.desc()).all()

@router.get("/all")
def admin_get_all(
    status: SosStatus | None = Query(None),
    zone_id: int | None = Query(None),
    conn=Depends(db_connection)
):
    return get_filtered_requests(status.value if status else None, zone_id, conn)


