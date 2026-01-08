from enum import Enum

class DisasterType(str, Enum):
    FLOOD = "FLOOD"
    EARTHQUAKE = "EARTHQUAKE"
    LANDSLIDE = "LANDSLIDE"
    TORNADO = "TORNADO"
    SINKHOLE = "SINKHOLE"
    TSUNAMI = "TSUNAMI"
    WILDFIRE = "WILDFIRE"
    BLIZZARD = "BLIZZARD"