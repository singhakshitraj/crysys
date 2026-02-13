from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    Numeric,
    Enum,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship
from .base import Base
from .enums import DisasterType,SosStatus

class SOSRequest(Base):
    __tablename__ = "sos_requests"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now()
    )

    disaster_type = Column(
        Enum(
            DisasterType,
            name="all_disaster_type",
            create_type=False
        )
    )

    latitude = Column(Numeric(38, 2))
    longitude = Column(Numeric(38, 2))

    message = Column(String(255))

    status = Column(
        Enum(
            SosStatus,
            name="all_sos_status",
            create_type=False
        )
    )

    updated_at = Column(DateTime(timezone=False))

    zone_id = Column(
        BigInteger,
        ForeignKey(
            "disaster_zone.id",
            ondelete="CASCADE"
        )
    )

    user_id = Column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )
    disaster_zone = relationship("DisasterZone", back_populates="sos_requests")
    user = relationship("User", back_populates="sos_requests")
