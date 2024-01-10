from dataclasses import dataclass
from datetime import date
from datetime import datetime
from typing import NoReturn
from typing import Optional


@dataclass
class Category:
    id: int
    name: str
    parent_id: int


@dataclass
class Series:
    id: str
    realtime_start: date
    realtime_end: date
    title: str
    observation_start: date
    observation_end: date
    frequency: str
    frequency_short: str
    units: str
    units_short: str
    seasonal_adjustment: str
    seasonal_adjustment_short: str
    last_updated: datetime
    popularity: int
    # group_popularity: int
    notes: Optional[str] = None

    def __post_init__(self) -> NoReturn:
        self.realtime_start = datetime.strptime(str(self.realtime_start), "%Y-%m-%d").date()
        self.realtime_end = datetime.strptime(str(self.realtime_end), "%Y-%m-%d").date()
        self.observation_start = datetime.strptime(str(self.observation_start), "%Y-%m-%d").date()
        self.observation_end = datetime.strptime(str(self.observation_end), "%Y-%m-%d").date()
        self.last_updated = datetime.strptime(str(self.last_updated) + "00", "%Y-%m-%d %H:%M:%S%z")


@dataclass
class Tag:
    name: str
    group_id: str
    notes: str
    created: datetime
    popularity: int
    series_count: int


@dataclass
class Release:
    id: int
    realtime_start: date
    realtime_end: date
    name: str
    press_release: bool
    link: str

    def __post_init__(self) -> NoReturn:
        self.realtime_start = datetime.strptime(str(self.realtime_start), "%Y-%m-%d").date()
        self.realtime_end = datetime.strptime(str(self.realtime_end), "%Y-%m-%d").date()


@dataclass
class ReleaseDate:
    release_id: int
    release_name: str
    date: date


@dataclass
class Source:
    id: int
    realtime_start: date
    realtime_end: date
    name: str
    link: str

    def __post_init__(self) -> NoReturn:
        self.realtime_start = datetime.strptime(str(self.realtime_start), "%Y-%m-%d").date()
        self.realtime_end = datetime.strptime(str(self.realtime_end), "%Y-%m-%d").date()


@dataclass
class Observation:
    realtime_start: date
    realtime_end: date
    date: date
    value: float


@dataclass
class SeriesGroup:
    title: str
    region_type: str
    series_group: str
    season: str
    units: str
    frequency: str
    min_date: date
    max_date: date

    # is in the specification, but not in the api response (?)
    # geom_type: str = None
    # group_id: int = None
    # min_start_date: date = None
    # max_start_date: date = None

    def __post_init__(self) -> NoReturn:
        # self.group_id = int(self.group_id) if self.group_id is not None else None
        # self.min_start_date = date(self.min_start_date) if self.min_start_date is not None else None
        # self.max_start_date = date(self.max_start_date) if self.max_start_date is not None else None
        self.min_date = datetime.strptime(str(self.min_date), "%Y-%m-%d").date()
        self.max_date = datetime.strptime(str(self.max_date), "%Y-%m-%d").date()
