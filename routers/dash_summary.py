from fastapi import APIRouter,Depends,Query
from models.enums import DangerLevel,SosStatus,DisasterType
from utils.validation_models.sos_request import SosRequestDto
from datetime import date,timedelta
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_
from datetime import date, timedelta, datetime
from models.disaster_zones import DisasterZone
from models.sos_requests import SOSRequest
from config.db import db_connection

router=APIRouter(
    prefix='/dashboard'
)
def count_active_or_null_zones(db: Session) -> int:
    stmt = select(func.count()).select_from(DisasterZone).where(
        or_(
            DisasterZone.is_active.is_(True),
            DisasterZone.is_active.is_(None),
        )
    )
    return db.scalar(stmt) or 0

def count_zones_by_danger_level(
    db: Session,
    danger_level: DangerLevel
) -> int:

    stmt = select(func.count()).where(
        DisasterZone.danger_level == danger_level
    )

    return db.scalar(stmt) or 0

def count_sos_by_status(db: Session, status: SosStatus) -> int:
    stmt = select(func.count()).where(
        SOSRequest.status == status
    )
    return db.scalar(stmt) or 0

@router.get("/summary")
def summary(db: Session = Depends(db_connection)):

    total_zones = len(DisasterType)
    active_disasters = count_active_or_null_zones(db)
    critical_zones = count_zones_by_danger_level(db, DangerLevel.HIGH)
    pending_sos_requests = count_sos_by_status(db, SosStatus.PENDING)

    return {
        "totalZones": total_zones,
        "activeDisasters": active_disasters,
        "criticalZones": critical_zones,
        "pendingSos": pending_sos_requests,
    }

def find_recent_sos_requests(
    db: Session,
    limit: int = 11
):
    stmt = (
        select(
            SOSRequest.id,
            SOSRequest.message,
            SOSRequest.latitude,
            SOSRequest.longitude,
            SOSRequest.status,
            SOSRequest.disaster_type,
            SOSRequest.created_at,
            SOSRequest.zone_id,
        )
        .order_by(SOSRequest.created_at.desc())
        .limit(limit)
    )

    rows = db.execute(stmt).mappings().all()
    return rows

def get_recent_sos_requests(db: Session) -> list[SosRequestDto]:
    rows = find_recent_sos_requests(db)
    return [SosRequestDto(**row) for row in rows]

@router.get("/recent-sos")
def recentsos(db: Session = Depends(db_connection)):
    return get_recent_sos_requests(db)

def count_sos_created_between(
    db: Session,
    start_ts,
    end_ts
) -> int:

    stmt = select(func.count()).where(
        SOSRequest.created_at >= start_ts,
        SOSRequest.created_at < end_ts,
    )

    return db.scalar(stmt) or 0

def count_active_or_null_zones_created_between(
    db: Session,
    start_ts,
    end_ts
) -> int:

    stmt = select(func.count()).where(
        DisasterZone.created_at >= start_ts,
        DisasterZone.created_at < end_ts,
        or_(
            DisasterZone.is_active.is_(True),
            DisasterZone.is_active.is_(None),
        ),
    )

    return db.scalar(stmt) or 0

def get_disaster_sos_stats(db: Session, days: int) -> dict[str, list]:

    today = date.today()
    start_date = today - timedelta(days=days - 1)

    dates = []
    active_disasters = []
    sos_counts = []

    for i in range(days):
        current_date = start_date + timedelta(days=i)

        start_ts = datetime.combine(current_date, datetime.min.time())
        end_ts = start_ts + timedelta(days=1)

        dates.append(current_date.isoformat())

        sos_counts.append(
            count_sos_created_between(db, start_ts, end_ts)
        )

        active_disasters.append(
            count_active_or_null_zones_created_between(
                db, start_ts, end_ts
            )
        )

    return {
        "dates": dates,
        "activeDisasters": active_disasters,
        "sosCounts": sos_counts,
    }

@router.get("/stats")
def get_stats(
    db: Session = Depends(db_connection),
    days: int = Query(default=7, ge=1, le=365),
):
    return get_disaster_sos_stats(db, days)
