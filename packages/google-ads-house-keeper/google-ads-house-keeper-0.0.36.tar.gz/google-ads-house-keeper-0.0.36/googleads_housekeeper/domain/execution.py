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

from typing import Type
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class ExecutionTypeEnum(Enum):
    SCHEDULED = 0
    MANUAL = 1


@dataclass
class Execution:
    task: int
    start_time: datetime
    end_time: datetime
    placements_excluded: int
    type: ExecutionTypeEnum
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self) -> None:
        self.type = self._cast_to_enum(ExecutionTypeEnum, self.type)

    def _cast_to_enum(self, enum: Type[Enum], value: str | Enum) -> Enum:
        return enum[value] if isinstance(value, str) else value


@dataclass
class ExecutionDetails:
    execution_id: str
    placement: str
    placement_type: str
    reason: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
