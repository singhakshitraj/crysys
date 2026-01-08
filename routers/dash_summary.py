from fastapi import APIRouter,Depends,Query
from psycopg2.extensions import connection
from utils.enums.danger_level import DangerLevel
from utils.enums.sos_status import SosStatus
from utils.enums.disaster_type import DisasterType
from config.db import db_connect
from utils.validation_models.sos_request import SosRequestDto
from psycopg2.extras import RealDictCursor
from datetime import date,timedelta
import datetime

router=APIRouter(
    prefix='/dashboard'
)
def count_active_or_null_zones(conn: connection) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM disaster_zone
            WHERE is_active = TRUE OR is_active IS NULL
        """)
        vals=cur.fetchone().get('count')
        return vals


def count_zones_by_danger_level(conn: connection, danger_level: DangerLevel) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM disaster_zone
            WHERE danger_level = %s
        """, (danger_level.value,))
        vals=cur.fetchone().get('count')
        return vals

def count_sos_by_status(conn: connection, status: SosStatus) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM sos_requests
            WHERE status = %s
        """, (status.value,))
        vals=cur.fetchone().get('count')
        return vals

@router.get('/summary')
def summary(conn=Depends(db_connect)):
    try:
        total_zones = len(DisasterType)
        active_disasters = count_active_or_null_zones(conn)
        critical_zones = count_zones_by_danger_level(conn, DangerLevel.HIGH)
        pending_sos_requests = count_sos_by_status(conn, SosStatus.PENDING)

        return {
            "total_zones":total_zones,
            "active_disasters":active_disasters,
            "critical_zones":critical_zones,
            "pending_sos_requests":pending_sos_requests
        }
    finally:
        conn.close()

def find_recent_sos_requests(conn: connection, limit: int = 11):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                id,message,
                latitude,longitude,
                status,disaster_type,
                created_at,zone_id
            FROM sos_requests
            ORDER BY created_at DESC
            LIMIT %s
        """, (limit,))
        return cur.fetchall()

def get_recent_sos_requests(conn:connection) -> list[SosRequestDto]:
    try:
        rows = find_recent_sos_requests(conn)
        return [SosRequestDto(**row) for row in rows]
    finally:
        conn.close()

@router.get('/recent-sos')
def recentsos(conn=Depends(db_connect)):
    return get_recent_sos_requests(conn)

def count_sos_created_between(conn: connection,start_ts,end_ts) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM sos_requests
            WHERE created_at >= %s
              AND created_at < %s
        """, (start_ts, end_ts))
        vals=cur.fetchone().get('count')
        return vals


def count_active_or_null_zones_created_between(conn: connection,start_ts,end_ts) -> int:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM disaster_zone
            WHERE created_at >= %s
              AND created_at < %s
              AND (is_active = TRUE OR is_active IS NULL)
        """, (start_ts, end_ts))
        vals=cur.fetchone().get('count')
        return vals

def get_disaster_sos_stats(conn,days: int) -> dict[str, list]:
    today = date.today()
    start_date = today - timedelta(days=days - 1)

    dates: list[str] = []
    active_disasters: list[int] = []
    sos_counts: list[int] = []

    try:
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            start_ts = datetime.datetime.combine(current_date, datetime.datetime.min.time())
            end_ts = start_ts + timedelta(days=1)
            dates.append(current_date.isoformat())
            sos_count = count_sos_created_between(
                conn, start_ts, end_ts
            )
            sos_counts.append(sos_count)
            disaster_count = count_active_or_null_zones_created_between(
                conn, start_ts, end_ts
            )
            active_disasters.append(disaster_count)

        return {
            "dates": dates,
            "activeDisasters": active_disasters,
            "sosCounts": sos_counts
        }
    finally:
        conn.close()

@router.get("/stats")
def get_stats(conn=Depends(db_connect),days: int = Query(default=7, ge=1, le=365)):
    return get_disaster_sos_stats(conn,days)
