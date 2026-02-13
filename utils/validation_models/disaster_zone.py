from pydantic import BaseModel
from datetime import datetime
from models.enums import DangerLevel,DisasterType

class DisasterZoneDto(BaseModel):
    id: int
    name: str
    disaster_type: DisasterType
    danger_level: DangerLevel
    is_active: bool | None
    created_at: datetime

class CreateDisasterZoneRequest(BaseModel):
    name: str
    disaster_type: DisasterType
    danger_level: DangerLevel
    center_latitude: float
    center_longitude: float
    radius: float
    
class CreateDisasterZoneDto(BaseModel):
    name: str
    disaster_type: DisasterType
    danger_level: DangerLevel
    center_latitude: float
    center_longitude: float
    radius: float
    
class UpdateDisasterZoneDto(BaseModel):
    name: str
    disaster_type: DisasterType
    danger_level: DangerLevel
    latitude: float
    longitude: float
    radius: float