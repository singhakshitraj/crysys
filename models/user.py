from sqlalchemy import Column, BigInteger, String, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .enums import *

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20))

    role = Column(
        Enum(RoleEnum, name="all_roles"),
        default=RoleEnum.USER
    )
    sos_requests = relationship(
        "SOSRequest",
        back_populates="user",
        cascade="all, delete"
    )
