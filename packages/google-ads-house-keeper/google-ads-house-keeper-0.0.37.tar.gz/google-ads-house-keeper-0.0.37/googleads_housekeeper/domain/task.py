# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from typing import Type
from collections import abc
from croniter import croniter
from dataclasses import asdict, dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import math
import uuid

from googleads_housekeeper.services.enums import ExclusionLevelEnum


class TaskStatus(Enum):
    ACTIVE = 0
    INACTIVE = 1


class TaskOutput(Enum):
    NOTIFY = 1
    EXCLUDE = 2
    EXCLUDE_AND_NOTIFY = 3


@dataclass
class Task:
    name: str
    exclusion_rule: str
    customer_ids: str
    date_range: int = 7
    from_days_ago: int = 0
    exclusion_level: ExclusionLevelEnum = ExclusionLevelEnum.AD_GROUP
    placement_types: str | None = None
    output: TaskOutput = TaskOutput.EXCLUDE_AND_NOTIFY
    status: TaskStatus = TaskStatus.ACTIVE
    schedule: str | None = None
    creation_date: datetime = datetime.now()
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        self.output = self._cast_to_enum(TaskOutput, self.output)
        self.status = self._cast_to_enum(TaskStatus, self.status)
        self.exclusion_level = self._cast_to_enum(ExclusionLevelEnum,
                                                  self.exclusion_level)

    def to_dict(self) -> dict:
        task_dict = {}
        for key, value in asdict(self).items():
            if hasattr(value, "value"):
                task_dict[key] = value.name
            else:
                task_dict[key] = value
        return task_dict

    @property
    def cron_schedule(self) -> str | None:
        minute = self.creation_date.strftime("%M")
        hour = self.creation_date.strftime("%H")

        if not (schedule := self.schedule) or self.schedule == "0":
            return None
        if 0 < int(schedule) < 24:
            schedule = f"{minute} */{schedule} * * *"
        elif int(schedule) >= 24:
            days = math.floor(int(self.schedule) / 24)
            schedule = f"{minute} {hour} */{days} * *"
        return schedule

    @property
    def start_date(self) -> str:
        return (
            datetime.now() -
            timedelta(days=int(self.date_range))).date().strftime("%Y-%m-%d")

    @property
    def end_date(self) -> str:
        return (datetime.now() - timedelta(days=int(self.from_days_ago))
                ).date().strftime("%Y-%m-%d")

    def get_start_end_date(self) -> tuple[str, str]:
        return self.start_date, self.end_date

    @property
    def accounts(self) -> list[str]:
        return self.customer_ids.split(",") if isinstance(
            self.customer_ids, str) else self.customer_ids

    @property
    def next_run(self) -> str:
        if not (schedule := self.cron_schedule):
            return "Not scheduled"
        return croniter(
            schedule,
            datetime.now()).get_next(datetime).strftime("%Y-%m-%d %H:%M")

    def _cast_to_enum(self, enum: Type[Enum], value: str | Enum) -> Enum:
        return enum[value] if isinstance(value, str) else value
