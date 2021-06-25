from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class Location:
    guid: str
    displayName: str


@dataclass(frozen=True)
class Event:
    displayName: str
    startTime: datetime
    endTime: datetime
    siteId: int
    locationGuid: str
    totalPlaces: int
    availablePlaces: int


@dataclass(frozen=True)
class LeisureCentre:
    siteId: int
    displayName: str
    locations: List[Location]
