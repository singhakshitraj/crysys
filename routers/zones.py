from fastapi import APIRouter,Depends,status
from psycopg2.extensions import connection
from psycopg2.extras import  RealDictCursor
from utils.validation_models.disaster_zone import DisasterZoneDto,CreateDisasterZoneDto
from config.db import db_connect

router=APIRouter()

@router.get('/zones')
def summary(conn=Depends(db_connect)):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT *
            FROM disaster_zone
            ORDER BY created_at DESC
        """)
        return cur.fetchall()


@router.post("/admin/zones",status_code=status.HTTP_201_CREATED)
def create_disaster_zone(req: CreateDisasterZoneDto,db: connection = Depends(db_connect)):
    print(req)
    print(str(req.disaster_type.value))
    query = """
        INSERT INTO disaster_zone
        (name, disaster_type, danger_level, latitude, longitude, radius)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, name, disaster_type, danger_level,
                  latitude, longitude, radius;
    """
    with db.cursor() as cursor:
        cursor.execute(
            query,
            (
                req.name,
                req.disaster_type.value,
                req.danger_level.value,
                req.center_latitude,
                req.center_longitude,
                req.radius,
            )
        )
        row = cursor.fetchone()
        db.commit()
    return {
        'status':'201',
        'data':row
    }
