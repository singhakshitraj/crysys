from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from enum import Enum
from utils.enums.sos_status import SosStatus
from utils.enums.disaster_type import DisasterType


class SosRequestDto(BaseModel):
    id: int
    message: str | None
    latitude: Decimal | None
    longitude: Decimal | None
    status: SosStatus
    disaster_type: DisasterType
    created_at: datetime
    zone_id: int | None
