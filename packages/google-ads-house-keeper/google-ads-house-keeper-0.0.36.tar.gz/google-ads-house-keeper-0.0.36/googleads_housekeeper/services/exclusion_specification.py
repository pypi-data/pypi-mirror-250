# Copyright 2022 Google LLC
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
from typing import Any
from collections.abc import Sequence
from copy import deepcopy
from dataclasses import asdict
import itertools
import re
from gaarf.report import GaarfReport, GaarfRow
import logging

from .external_parsers.base_parser import BaseParser, NullParser
from .external_parsers.website_parser import WebSiteParser
from .external_parsers.youtube_data_parser import ChannelInfoParser, VideoInfoParser
from .enums import PlacementTypeEnum, ExclusionTypeEnum
from .unit_of_work import AbstractUnitOfWork

PARSEABLE = ("WEBSITE", "YOUTUBE_VIDEO", "YOUTUBE_CHANNEL")


class BaseExclusionSpecification:

    def __init__(self,
                 expression: str,
                 exclusion_type: ExclusionTypeEnum | None = None,
                 parser: type[BaseParser] = NullParser,
                 placement_type: PlacementTypeEnum | None = None,
                 repository_name: str | None = None):
        """Constructor for the class.

        Args:
            expression: exclusion expression in a form of `name > value`
            exclusion_type: type of the exclusion
            parser: parser for getting data from API and/or DB
        """
        elements = [
            element.strip() for element in expression.split(" ", maxsplit=2)
        ]
        if len(elements) != 3:
            raise ValueError(
                "Incorrect expression, specify in 'name > value' format")
        if elements[1] not in (">", ">=", "<", "<=", "=", "!=", "regexp",
                               "contains"):
            raise ValueError(
                "Incorrect operator for expression, "
                "only '>', '>=', '<', '<=', '=', '!=', 'regexp', 'contains' are supported"
            )

        self.name = elements[0]
        self.operator = "==" if elements[1] == "=" else elements[1]
        self.value = elements[2].replace("'", "").replace('"', '')
        self.exclusion_type = exclusion_type
        self.parser = parser
        self.corresponding_placement_type = placement_type
        self.repository_name = repository_name

    def is_satisfied_by(
            self,
            placement_info: GaarfRow,
            uow: AbstractUnitOfWork | None = None) -> tuple[bool, Any]:
        matching_placement = {}
        with uow:
            if (placement_info.placement_type in PARSEABLE and
                    self.exclusion_type != ExclusionTypeEnum.GOOGLE_ADS_INFO):
                if placement := getattr(uow,
                                        self.repository_name).get_by_condition(
                                            "placement",
                                            placement_info.placement):
                    placement = placement[0]
                    matching_placement = asdict(placement)
                else:
                    # Haven't found a placement in DB, cannot apply the rule
                    return False, matching_placement
            else:
                placement = placement_info
            if not hasattr(placement, self.name):
                raise ValueError(f"{self.name} is not found!")
            if hasattr(placement,
                       "is_processed") and not placement.is_processed:
                logging.debug(
                    "Cannot get internal information on %s placement of type %s",
                    placement_info.placement, placement_info.placement_type)
                return False, matching_placement
            else:
                if self.operator in ("regexp", "contains"):
                    return self._check_regexp(placement), matching_placement
                return self._eval_expression(placement), matching_placement

    def _check_regexp(self, placement) -> bool:
        if placement_element := getattr(placement, self.name):
            return bool(
                re.search(fr"{self.value}", placement_element, re.IGNORECASE))
        else:
            return False

    def _eval_expression(self, placement):
        try:
            value = float(self.value)
        except ValueError:
            value = self.value
        if isinstance(value, float):
            return eval(
                f"{getattr(placement, self.name)}{self.operator} {value}")
        return eval(
            f"'{getattr(placement, self.name)}' {self.operator} '{value}'")

    def __str__(self):
        return f"{self.exclusion_type.name}:{self.name} {self.operator} {self.value}"

    def __repr__(self):
        return f"{self.__class__.__name__}(exclusion_type='{self.exclusion_type.name}', name='{self.name}', operator='{self.operator}', value='{self.value}')"

    def __eq__(self, other):
        return (self.exclusion_type, self.name, self.operator,
                self.value) == (other.exclusion_type, other.name,
                                other.operator, other.value)


class AdsExclusionSpecification(BaseExclusionSpecification):
    """Class for specifying exclusion rules."""

    def __init__(self, expression):
        super().__init__(expression,
                         exclusion_type=ExclusionTypeEnum.GOOGLE_ADS_INFO)


class ContentExclusionSpecification(BaseExclusionSpecification):

    def __init__(self, expression) -> None:
        super().__init__(expression=expression,
                         exclusion_type=ExclusionTypeEnum.WEBSITE_INFO,
                         parser=WebSiteParser,
                         placement_type=PlacementTypeEnum.WEBSITE,
                         repository_name="website_info")


class YouTubeChannelExclusionSpecification(BaseExclusionSpecification):

    def __init__(self, expression) -> None:
        super().__init__(expression=expression,
                         exclusion_type=ExclusionTypeEnum.YOUTUBE_CHANNEL_INFO,
                         parser=ChannelInfoParser,
                         placement_type=PlacementTypeEnum.YOUTUBE_CHANNEL,
                         repository_name="youtube_channel_info")


class YouTubeVideoExclusionSpecification(BaseExclusionSpecification):

    def __init__(self, expression) -> None:
        super().__init__(expression=expression,
                         exclusion_type=ExclusionTypeEnum.YOUTUBE_VIDEO_INFO,
                         parser=VideoInfoParser,
                         placement_type=PlacementTypeEnum.YOUTUBE_VIDEO,
                         repository_name="youtube_video_info")


class Specification:

    def __init__(self, uow: AbstractUnitOfWork | None = None):
        self.uow = uow
        self.allowed_placement_types = set([p.name for p in PlacementTypeEnum])

    def apply_specifications(self, specifications: Sequence[
        Sequence[BaseExclusionSpecification]],
                             placements: GaarfReport) -> GaarfReport | None:
        """Get placements that satisfy exclusion specifications."""
        to_be_excluded_placements = []
        with self.uow as uow:
            for placement in placements:
                is_allowlisted = False
                reason, matching_placement = self.satisfies(
                    specifications, placement)
                if reason:
                    reason_str = ",".join(list(itertools.chain(*reason)))
                    if uow.allowlisting.get_by_conditions({
                            "name":
                            placement.placement,
                            "type":
                            placement.placement_type,
                            "account_id":
                            placement.customer_id
                    }):
                        is_allowlisted = True
                    to_be_excluded_placements.append(
                        placement.data +
                        [reason_str, matching_placement, is_allowlisted])
        if to_be_excluded_placements:
            return GaarfReport(results=to_be_excluded_placements,
                               column_names=placements.column_names +
                               ["reason", "extra_info", "allowlist"])
        return None

    def satisfies(self, specs: Sequence[Sequence[BaseExclusionSpecification]],
                  placement: GaarfRow) -> tuple[list[str], list[str]]:
        rules_satisfied: list[str] = []
        placement_satisfied: dict = {}
        for spec_entry in specs:
            spec_satisfied: list[str] = []
            safisfied_placement = None
            for spec in spec_entry:
                if spec.exclusion_type != ExclusionTypeEnum.GOOGLE_ADS_INFO:
                    formatted_exclusion_type = spec.exclusion_type.name.replace(
                        "_INFO", "")
                    if formatted_exclusion_type != placement.placement_type:
                        continue
                is_satisfied, placement_satisfied = spec.is_satisfied_by(
                    placement, self.uow)
                if is_satisfied:
                    spec_satisfied.append(str(spec))
                    continue
                else:
                    break
            if len(spec_satisfied) == len(spec_entry):
                rules_satisfied.append(spec_satisfied)
        return rules_satisfied, placement_satisfied


class NullSpecification(BaseExclusionSpecification):

    def __init__(self, type, expression):
        super().__init__(type)
        raise ValueError(f"Incorrect type of rule: {type}")


class SpecificationFactory:

    def create_specification(self, type: str,
                             condition: str) -> BaseExclusionSpecification:
        if type == "GOOGLE_ADS_INFO":
            return AdsExclusionSpecification(condition)
        if type == "WEBSITE_INFO":
            return ContentExclusionSpecification(condition)
        if type == "YOUTUBE_CHANNEL_INFO":
            return YouTubeChannelExclusionSpecification(condition)
        if type == "YOUTUBE_VIDEO_INFO":
            return YouTubeVideoExclusionSpecification(condition)
        else:
            return NullSpecification(type, condition)
