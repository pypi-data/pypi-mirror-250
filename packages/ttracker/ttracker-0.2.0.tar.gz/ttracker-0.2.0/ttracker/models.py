from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Task:
    name: str
    start_active_timestamp: Optional[datetime]
    visible: bool = field(default=True)
    cumulative_time: int = field(default=0)
    last_modified: datetime = field(default=datetime.now())

    @property
    def active(self) -> bool:
        return self.start_active_timestamp is not None

    def to_row(self):
        return [
            self.name,
            self.start_active_timestamp,
            self.visible,
            self.cumulative_time,
        ]

    @staticmethod
    def to_header():
        return [
            "name",
            "start_active_timestamp",
            "visible",
            "cumulative_time",
        ]
