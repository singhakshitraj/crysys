from pydantic import BaseModel
from datetime import datetime
from utils.enums.danger_level import DangerLevel
from utils.enums.disaster_type import DisasterType

class DisasterZoneDto(BaseModel):
    id: int
    name: str
    disaster_type: DisasterType
    danger_level: DangerLevel
    is_active: bool | None
    created_at: datetime
