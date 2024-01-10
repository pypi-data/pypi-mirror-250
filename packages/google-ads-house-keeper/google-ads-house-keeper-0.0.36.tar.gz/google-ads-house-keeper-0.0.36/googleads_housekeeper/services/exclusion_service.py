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
from collections import defaultdict
from collections.abc import Iterable, Sequence

from typing import Any

from copy import deepcopy
from dataclasses import dataclass
import logging
from gaarf.api_clients import GoogleAdsApiClient
from gaarf.base_query import BaseQuery
from gaarf.report import GaarfRow, GaarfReport
from gaarf.query_executor import AdsReportFetcher
from google.api_core import exceptions
from tenacity import Retrying, RetryError, retry_if_exception_type, stop_after_attempt, wait_exponential

from .exclusion_specification import Specification, BaseExclusionSpecification
from .enums import PlacementTypeEnum, ExclusionLevelEnum


class NegativePlacementsLists(BaseQuery):

    def __init__(self):
        self.query_text = f"""
            SELECT
                shared_set.name AS name,
                shared_set.resource_name AS resource_name
            FROM shared_set
            WHERE shared_set.type = 'NEGATIVE_PLACEMENTS'
            AND shared_set.status = 'ENABLED'
        """


@dataclass
class ExclusionResult:
    excluded_placements: int = 0
    associated_with_list_placements: int = 0


class PlacementExcluder:
    """Class for excluding placements based on a sequence of exclusion specifications."""

    def __init__(self, client: GoogleAdsApiClient, uow=None):
        self._client = client
        self.client = client.client
        self.uow = uow

    def exclude_placements(
        self,
        to_be_excluded_placements: GaarfReport,
        exclusion_level: ExclusionLevelEnum = ExclusionLevelEnum.AD_GROUP
    ) -> ExclusionResult:
        """Excludes placements and optionally returns placements which cannot be excluded."""
        excluded_placements_count = 0
        associated_placements_count = 0
        self._init_criterion_service_and_operation(exclusion_level)
        # TODO: Terrible unpacking, refactor
        report_fetcher = AdsReportFetcher(self._client)
        customer_ids = to_be_excluded_placements["customer_id"].to_list(
            flatten=True, distinct=True)
        negative_placements_list = report_fetcher.fetch(
            NegativePlacementsLists(), customer_ids)
        exclusion_operations, shared_set_operations_mapping, campaign_set_mapping_operations = (
            self.
            _create_placement_exclusion_operations_and_non_excluded_placements(
                to_be_excluded_placements, exclusion_level,
                negative_placements_list))
        if shared_set_operations_mapping:
            for customer_id, operations in shared_set_operations_mapping.items(
            ):
                try:
                    if operations:
                        self._add_placements_to_shared_set(
                            customer_id, operations)
                        # TODO: provide meaningful message
                        # TODO: display in UI where connection should be made
                        logging.info(
                            "Added %d placements to shared_set for %d account",
                            len(operations), customer_id)
                        associated_placements_count += len(operations)
                except Exception as e:
                    logging.error(e)
        if exclusion_operations:
            for customer_id, operations in exclusion_operations.items():
                try:
                    if operations:
                        self._exclude(customer_id, operations)
                        logging.info("Excluded %d placements from account %s",
                                     len(operations), customer_id)
                        excluded_placements_count += len(operations)
                except Exception as e:
                    logging.error(e)
            logging.info("%d placements was excluded",
                         excluded_placements_count)
        return ExclusionResult(
            excluded_placements=excluded_placements_count,
            associated_with_list_placements=associated_placements_count)

    def _init_criterion_service_and_operation(
            self, exclusion_level: ExclusionLevelEnum) -> None:
        # Init services for ShareSets
        self.shared_set_service = self.client.get_service("SharedSetService")
        self.shared_criterion_service = self.client.get_service(
            "SharedCriterionService")
        self.campaign_shared_set_service = self.client.get_service(
            "CampaignSharedSetService")
        self.shared_set_operation = self.client.get_type("SharedSetOperation")

        if exclusion_level == ExclusionLevelEnum.CAMPAIGN:
            self.criterion_service = self.client.get_service(
                "CampaignCriterionService")
            self.criterion_operation = self.client.get_type(
                "CampaignCriterionOperation")
            self.criterion_path_method = self.criterion_service.campaign_criterion_path
            self.mutate_operation = self.criterion_service.mutate_campaign_criteria
            self.entity_name = "campaign_id"
        if exclusion_level == ExclusionLevelEnum.AD_GROUP:
            self.criterion_service = self.client.get_service(
                "AdGroupCriterionService")
            self.criterion_operation = self.client.get_type(
                "AdGroupCriterionOperation")
            self.criterion_path_method = self.criterion_service.ad_group_criterion_path
            self.mutate_operation = self.criterion_service.mutate_ad_group_criteria
            self.entity_name = "ad_group_id"
        if exclusion_level == ExclusionLevelEnum.ACCOUNT:
            self.criterion_service = self.client.get_service(
                "CustomerNegativeCriterionService")
            self.criterion_operation = self.client.get_type(
                "CustomerNegativeCriterionOperation")
            self.criterion_path_method = self.criterion_service.customer_negative_criterion_path
            self.mutate_operation = self.criterion_service.mutate_customer_negative_criteria
            self.entity_name = "customer_id"

    def _create_placement_exclusion_operations_and_non_excluded_placements(
        self, placements: GaarfReport, exclusion_level: ExclusionLevelEnum,
        negative_placements_list: GaarfReport
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        """Generates exclusion operations on customer_id level and get all placements that cannot be excluded."""
        operations_mapping: dict[str, Any] = {}
        shared_set_operations_mapping: dict[str, Any] = {}
        campaign_set_operations_mapping: dict[str, Any] = {}
        allowlisted_placements: dict[int, list[str]] = defaultdict(list)
        with self.uow as uow:
            for allowlisted_placement in uow.allowlisting.list():
                allowlisted_placements[int(
                    allowlisted_placement.account_id)].append(
                        allowlisted_placement.name)

        for placement_info in placements:
            if (placement_info.customer_id in allowlisted_placements
                    and placement_info.placement
                    in allowlisted_placements[placement_info.customer_id]):
                continue
            # TODO: customer_id is not relevant for share_set we need campaign_id
            # TODO: terrible unpacking return object instead
            customer_id, operation, is_shared_set = self._create_placement_operation(
                placement_info, exclusion_level, negative_placements_list)
            if is_shared_set:
                if isinstance(shared_set_operations_mapping.get(customer_id),
                              list):
                    shared_set_operations_mapping[customer_id].append(
                        operation)
                else:
                    shared_set_operations_mapping[customer_id] = [operation]
                continue
            if isinstance(operations_mapping.get(customer_id), list):
                operations_mapping[customer_id].append(operation)
            else:
                operations_mapping[customer_id] = [operation]
        return operations_mapping, shared_set_operations_mapping, campaign_set_operations_mapping

    def _create_placement_operation(
        self,
        placement_info: GaarfRow,
        exclusion_level: ExclusionLevelEnum,
        negative_placements_list: GaarfReport | None = None
    ) -> tuple[str, Any, bool]:
        "Creates exclusion operation for a single placement." ""
        entity_criterion = None
        is_shared_set = False
        if placement_info.campaign_type == "VIDEO" and exclusion_level in (
                ExclusionLevelEnum.CAMPAIGN, ExclusionLevelEnum.AD_GROUP):
            shared_set_resource_name = self._create_shared_set(
                placement_info.customer_id, placement_info.campaign_id,
                negative_placements_list)
            is_shared_set = True
            shared_criterion_operation = self.client.get_type(
                "SharedCriterionOperation")
            entity_criterion = shared_criterion_operation.create
            entity_criterion.shared_set = shared_set_resource_name

        if (placement_info.placement_type ==
                PlacementTypeEnum.MOBILE_APPLICATION.name):
            app_id = self._format_app_id(placement_info.placement)
        if not entity_criterion:
            entity_criterion = self.criterion_operation.create
        # Assign specific criterion
        if (placement_info.placement_type == PlacementTypeEnum.WEBSITE.name):
            entity_criterion.placement.url = placement_info.placement
        if (placement_info.placement_type ==
                PlacementTypeEnum.MOBILE_APPLICATION.name):
            entity_criterion.mobile_application.app_id = app_id
        if (placement_info.placement_type ==
                PlacementTypeEnum.YOUTUBE_VIDEO.name):
            entity_criterion.youtube_video.video_id = placement_info.placement
        if (placement_info.placement_type ==
                PlacementTypeEnum.YOUTUBE_CHANNEL.name):
            entity_criterion.youtube_channel.channel_id = placement_info.placement
        if exclusion_level == ExclusionLevelEnum.ACCOUNT:
            entity_criterion.resource_name = (self.criterion_path_method(
                placement_info.customer_id, placement_info.criterion_id))
        elif not is_shared_set:
            entity_criterion.negative = True
            entity_criterion.resource_name = (self.criterion_path_method(
                placement_info.customer_id,
                placement_info.get(self.entity_name),
                placement_info.criterion_id))
        if is_shared_set:
            operation = deepcopy(shared_criterion_operation)
        else:
            operation = deepcopy(self.criterion_operation)
        return placement_info.customer_id, operation, is_shared_set

    def _create_shared_set(
        self,
        customer_id: int,
        campaign_id: int,
        negative_placements_list: GaarfReport,
        base_share_set_name: str = "CPR Negative placements list - Campaign:"
    ) -> str:
        name = f"{base_share_set_name} {campaign_id}"
        exclusion_list = negative_placements_list.to_dict(
            key_column="name",
            value_column="resource_name",
            value_column_output="scalar")
        if name in exclusion_list:
            return exclusion_list[name]
        shared_set = self.shared_set_operation.create
        shared_set.name = name
        shared_set.type_ = self.client.enums.SharedSetTypeEnum.NEGATIVE_PLACEMENTS

        operation = deepcopy(self.shared_set_operation)
        shared_set_response = self.shared_set_service.mutate_shared_sets(
            customer_id=str(customer_id), operations=[operation])
        shared_set_resource_name = shared_set_response.results[0].resource_name
        logging.debug(f'Created shared set "{shared_set_resource_name}".')
        return shared_set_resource_name

    def _add_placements_to_shared_set(self, customer_id: int,
                                      operations: list):
        if not isinstance(operations, Iterable):
            operations = [operations]
        try:
            for attempt in Retrying(retry=retry_if_exception_type(
                    exceptions.InternalServerError),
                                    stop=stop_after_attempt(3),
                                    wait=wait_exponential()):
                with attempt:
                    self.shared_criterion_service.mutate_shared_criteria(
                        customer_id=str(customer_id), operations=operations)
        except RetryError as retry_failure:
            logging.error(
                "Cannot add placements to exclusion list for account '%s' %d times",
                customer_id, retry_failure.last_attempt.attempt_number)

    def _add_campaigns_to_share_set(self, customer_id: str,
                                    campaign_ids: list[str],
                                    share_set: str) -> None:
        campaign_service = self.client.get_service("CampaignService")
        campaign_set_operation = self.client.get_type(
            "CampaignSharedSetOperation")
        campaign_set = campaign_set_operation.create
        operations = []
        for campaign_id in campaign_ids:
            campaign_set.campaign = campaign_service.campaign_path(
                customer_id, campaign_id)
            campaign_set.shared_set = share_set
            operation = deepcopy(campaign_set_operation)
            operations.append(operation)
        self.campaign_shared_set_service.mutate_campaign_shared_sets(
            customer_id=customer_id, operations=operations)

    def _format_app_id(self, app_id: str) -> str:
        if app_id.startswith("mobileapp::"):
            criteria = app_id.split("-")
            app_id = criteria[-1]
            app_store = criteria[0].split("::")[-1]
            app_store = app_store.replace("mobileapp::1000", "")
            app_store = app_store.replace("1000", "")
            return f"{app_store}-{app_id}"
        return app_id

    def _exclude(self, customer_id: str, operations) -> None:
        """Applies exclusion operations for a single customer_id."""
        if not isinstance(operations, Iterable):
            operations = [operations]
        try:
            for attempt in Retrying(retry=retry_if_exception_type(
                    exceptions.InternalServerError),
                                    stop=stop_after_attempt(3),
                                    wait=wait_exponential()):
                with attempt:
                    self.mutate_operation(customer_id=str(customer_id),
                                          operations=operations)
        except RetryError as retry_failure:
            logging.error(
                "Cannot exclude placements for account '%s' %d times",
                customer_id, retry_failure.last_attempt.attempt_number)
