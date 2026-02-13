from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from enum import Enum
from models.enums import SosStatus,DisasterType


class SosRequestDto(BaseModel):
    id: int
    message: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    status: SosStatus
    disaster_type: DisasterType
    created_at: datetime
    zone_id: int | None

class CreateSosRequest(BaseModel):
    latitude: Decimal | None
    longitude: Decimal | None
    message: str
    disaster_type: DisasterType

class MessageResponse(BaseModel):
    message: str
