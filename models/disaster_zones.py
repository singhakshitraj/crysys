from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    DateTime,
    Boolean,
    String,
    Float,
    Enum,
    func
)
from .base import Base
from .enums import DangerLevel,DisasterType
from sqlalchemy.orm import relationship

class DisasterZone(Base):
    __tablename__ = "disaster_zone"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    latitude = Column(Numeric(38, 2))
    longitude = Column(Numeric(38, 2))
    created_at = Column(
        DateTime,
        server_default=func.now()
    )
    danger_level = Column(
        Enum(DangerLevel, name="all_danger_level", create_type=False)
    )
    disaster_type = Column(
        Enum(DisasterType, name="all_disaster_type", create_type=False)
    )
    is_active = Column(
        Boolean,
        nullable=False,
        server_default="true"
    )
    name = Column(String(255), nullable=False)
    radius = Column(Float, nullable=False)
    sos_requests = relationship(
        "SOSRequest",
        back_populates="disaster_zone",
        cascade="all, delete"
    )