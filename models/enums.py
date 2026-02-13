import enum

class RoleEnum(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class DangerLevel(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class DisasterType(enum.Enum):
    FLOOD = "FLOOD"
    EARTHQUAKE = "EARTHQUAKE"
    FIRE = "FIRE"
    CYCLONE='CYCLONE'
    DROUGHT='DROUGHT'
    LANDSLIDE='LANDSLIDE'
    TORNADO='TORNADO'
    SINKHOLE='SINKHOLE'
    TSUNAMI='TSUNAMI'
    WILDFIRE='WILDFIRE'
    BLIZZARD='BLIZZARD'


class SosStatus(enum.Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    ACCEPTED='ACCEPTED'
    REJECTED='REJECTED'