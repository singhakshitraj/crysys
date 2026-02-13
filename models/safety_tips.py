from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    Enum,
    ForeignKey,
    func
)
from .base import Base
from .enums import DisasterType
from sqlalchemy.orm import relationship

class SafetyTip(Base):
    __tablename__ = "safety_tip"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now()
    )
    description = Column(String(255))
    disaster_type = Column(
        Enum(
            DisasterType,
            name="all_disaster_type",
            create_type=False
        )
    )
    title = Column(String(255))
    disaster_zone_id = Column(
        Integer,
        ForeignKey("disaster_zone.id")
    )
    disaster_zone = relationship(
        "DisasterZone",
        back_populates="safety_tips"
    )
