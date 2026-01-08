from fastapi import APIRouter,Depends
from psycopg2.extensions import connection
from psycopg2.extras import  RealDictCursor
from utils.validation_models.disaster_zone import DisasterZoneDto
from config.db import db_connect

router=APIRouter()
def find_all_disaster_zones(conn: connection):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT
                id,
                name,
                disaster_type,
                danger_level,
                is_active,
                created_at
            FROM disaster_zone
            ORDER BY created_at DESC
        """)
        return cur.fetchall()

def get_all_disaster_zones(conn:connection) -> list[DisasterZoneDto]:
    try:
        rows = find_all_disaster_zones(conn)
        return [DisasterZoneDto(**row) for row in rows]

    finally:
        conn.close()

@router.get('/zones',response_model=list[DisasterZoneDto])
def summary(conn=Depends(db_connect)):
    return get_all_disaster_zones(conn)
