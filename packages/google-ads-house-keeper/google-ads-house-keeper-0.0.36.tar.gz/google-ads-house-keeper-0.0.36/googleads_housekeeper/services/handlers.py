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
from collections.abc import Sequence

from typing import Any, Callable
from dataclasses import asdict
from datetime import datetime, timedelta
from functools import reduce
import logging
import itertools
import json
from operator import add
import pickle
import sqlalchemy

from gaarf.api_clients import GoogleAdsApiClient
from gaarf.report import GaarfReport
from gaarf.query_executor import AdsReportFetcher

from googleads_housekeeper.domain import allowlisting, commands, events, execution, settings, task
from googleads_housekeeper.domain.placements import (Placements,
                                                     PlacementsConversionSplit,
                                                     aggregate_placements,
                                                     join_conversion_split)
from googleads_housekeeper.adapters import publisher

from . import unit_of_work
from .exclusion_service import ExclusionResult, PlacementExcluder
from .rules_parser import RulesParser
from .enums import ExclusionTypeEnum, ExclusionLevelEnum
from .exclusion_specification import BaseExclusionSpecification, Specification


def get_accessible_mcc_ids(
        cmd: commands.GetMccIds, uow: unit_of_work.AbstractUnitOfWork,
        ads_api_client: GoogleAdsApiClient) -> list[dict[str, str]]:
    api_client = ads_api_client.client
    customer_service = api_client.get_service("CustomerService")
    accessible_customers = customer_service.list_accessible_customers()
    mcc_ids = [
        resource.split('/')[1]
        for resource in accessible_customers.resource_names
    ]
    mcc_full = []
    for mcc in mcc_ids:
        report_fetcher = AdsReportFetcher(api_client=ads_api_client,
                                          customer_ids=mcc)
        try:
            mcc_data = report_fetcher.fetch("""
            SELECT
                customer_client.descriptive_name AS account_name,
                customer_client.id AS account_id
            FROM customer_client
            WHERE customer_client.manager = TRUE
            AND customer_client.status = "ENABLED"
            """)
            if mcc_data:
                mcc_full.append(mcc_data)
        except Exception:
            pass
    mcc_full = reduce(add, mcc_full)
    result = []
    with uow:
        for row in mcc_full:
            row_dict = {"id": row.account_id, "account_name": row.account_name}
            result.append(row_dict)
            uow.mcc_ids.add(settings.MccIds(**row_dict))
        try:
            uow.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
    return result


def get_customer_ids(
        cmd: commands.GetMccIds, uow: unit_of_work.AbstractUnitOfWork,
        ads_api_client: GoogleAdsApiClient) -> list[dict[str, int]]:
    report_fetcher = AdsReportFetcher(api_client=ads_api_client,
                                      customer_ids=cmd.mcc_id)
    customer_ids = report_fetcher.fetch("""
    SELECT
        customer_client.descriptive_name AS account_name,
        customer_client.id AS customer_id
    FROM customer_client
    WHERE customer_client.manager = FALSE
    AND customer_client.status = "ENABLED"
    """)
    result = []
    with uow:
        for row in customer_ids:
            result.append({
                "account_name": row.account_name,
                "id": row.customer_id
            })
            uow.customer_ids.add(
                settings.CustomerIds(mcc_id=cmd.mcc_id,
                                     account_name=row.account_name,
                                     id=str(row.customer_id)))
        try:
            uow.commit()
        except sqlalchemy.exc.IntegrityError:
            pass
    return result


def run_manual_exclusion_task(
        cmd: commands.RunManualExclusion, uow: unit_of_work.AbstractUnitOfWork,
        ads_api_client: GoogleAdsApiClient) -> dict[str, int]:
    with uow:
        placement_excluder = PlacementExcluder(ads_api_client, uow)
        exclusion_result = placement_excluder.exclude_placements(
            GaarfReport(results=cmd.placements, column_names=cmd.header))
    return asdict(exclusion_result)


def task_created(event: events.TaskCreated,
                 publisher: publisher.BasePublisher) -> None:
    publisher.publish("task_created", event)


def task_updated(event: events.TaskUpdated,
                 publisher: publisher.BasePublisher) -> None:
    publisher.publish("task_updated", event)


def task_deleted(event: events.TaskDeleted,
                 publisher: publisher.BasePublisher) -> None:
    publisher.publish("task_deleted", event)


def run_task(
        cmd: commands.RunTask,
        uow: unit_of_work.AbstractUnitOfWork,
        ads_api_client: GoogleAdsApiClient,
        publisher: publisher.BasePublisher
    | None = None,
        save_to_db: bool = True):
    n_excluded_placements = 0
    with uow:
        task_obj = uow.tasks.get(task_id=cmd.id)
        report_fetcher = AdsReportFetcher(api_client=ads_api_client)
        exclusion_specification = RulesParser().generate_specifications(
            task_obj.exclusion_rule)
        placement_excluder = PlacementExcluder(ads_api_client, uow)
        specification = Specification(uow)
        start_time = datetime.now()
        to_be_excluded_placements = find_placements_for_exclusion(
            task_obj, report_fetcher, specification, exclusion_specification)

        if to_be_excluded_placements and task_obj.output in (
                task.TaskOutput.EXCLUDE, task.TaskOutput.EXCLUDE_AND_NOTIFY):
            exclusion_result = placement_excluder.exclude_placements(
                to_be_excluded_placements, task_obj.exclusion_level)

            end_time = datetime.now()
            n_excluded_placements = exclusion_result.excluded_placements
        else:
            exclusion_result = ExclusionResult()
            end_time = datetime.now()
        execution_obj = execution.Execution(
            task=cmd.id,
            start_time=start_time,
            end_time=end_time,
            placements_excluded=n_excluded_placements,
            type=cmd.type)
        uow.executions.add(execution_obj)
        if save_to_db and n_excluded_placements:
            for placement in to_be_excluded_placements:
                if hasattr(placement, "reason"):
                    exclusion_reason = placement.reason
                else:
                    exclusion_reason = ""
                uow.execution_details.add(
                    execution.ExecutionDetails(
                        execution_id=execution_obj.id,
                        placement=placement.name,
                        placement_type=placement.placement_type,
                        reason=exclusion_reason))
        uow.commit()
        if task_obj.output in (task.TaskOutput.NOTIFY,
                               task.TaskOutput.EXCLUDE_AND_NOTIFY):
           publisher.publish("task_run", execution_obj)
        return asdict(exclusion_result)


def preview_placements(cmd: commands.PreviewPlacements,
                       uow: unit_of_work.AbstractUnitOfWork,
                       ads_api_client: GoogleAdsApiClient,
                       save_to_db: bool = True) -> dict[str, Any]:
    report_fetcher = AdsReportFetcher(api_client=ads_api_client)
    placement_excluder = PlacementExcluder(ads_api_client, uow)
    exclusion_specification = RulesParser().generate_specifications(
        cmd.exclusion_rule)
    task_obj = task.Task(name="",
                         exclusion_rule=cmd.exclusion_rule,
                         customer_ids=cmd.customer_ids,
                         date_range=cmd.date_range,
                         from_days_ago=cmd.from_days_ago,
                         exclusion_level=cmd.exclusion_level,
                         placement_types=cmd.placement_types)
    specification = Specification(uow)
    to_be_excluded_placements = find_placements_for_exclusion(
        task_obj, report_fetcher, specification, exclusion_specification,
        save_to_db)
    if not to_be_excluded_placements:
        data = {}
    else:
        data = json.loads(
            to_be_excluded_placements.to_pandas().to_json(orient="index"))
    return {
        "data": data,
        "dates": {
            "date_from": task_obj.start_date,
            "date_to": task_obj.end_date
        }
    }


def find_placements_for_exclusion(
        task: task.Task,
        report_fetcher: AdsReportFetcher,
        specification: Specification,
        exclusion_specification: Sequence[Sequence[BaseExclusionSpecification]]
    | None = None,
        save_to_db: bool = True) -> GaarfReport | None:
    runtime_options = RulesParser().define_runtime_options(
        exclusion_specification)
    start_date, end_date = task.get_start_end_date()
    reports: list[GaarfReport] = []
    for account in task.accounts:
        placement_query = Placements(placement_types=task.placement_types,
                                     start_date=start_date,
                                     end_date=end_date)
        placements = report_fetcher.fetch(placement_query,
                                          customer_ids=account)
        if "YOUTUBE_VIDEO" in task.placement_types:
            youtube_video_placement_query = Placements(
                placement_types=("YOUTUBE_VIDEO", ),
                placement_level_granularity="detail_placement_view",
                start_date=start_date,
                end_date=end_date)
            youtube_video_placements = report_fetcher.fetch(
                youtube_video_placement_query, customer_ids=account)
            placements = youtube_video_placements + placements

        if not placements:
            continue
        if runtime_options.is_conversion_query:
            conversion_split_query = PlacementsConversionSplit(
                placement_types=task.placement_types,
                start_date=start_date,
                end_date=end_date)
            placements_by_conversion_name = report_fetcher.fetch(
                conversion_split_query, customer_ids=account)
            if "YOUTUBE_VIDEO" in task.placement_types:
                youtube_video_conversion_split_query = PlacementsConversionSplit(
                    placement_types=("YOUTUBE_VIDEO", ),
                    placement_level_granularity="detail_placement_view",
                    start_date=start_date,
                    end_date=end_date)
                youtube_video_placements_by_conversion_name = report_fetcher.fetch(
                    youtube_video_conversion_split_query, customer_ids=account)
                placements_by_conversion_name = (
                    placements_by_conversion_name +
                    youtube_video_placements_by_conversion_name)
            if placements_by_conversion_name:
                placements_by_conversion_name = (
                    specification.apply_specifications(
                        [runtime_options.conversion_rules],
                        placements_by_conversion_name))
                placements = join_conversion_split(
                    placements, placements_by_conversion_name,
                    runtime_options.conversion_name)
        placements = aggregate_placements(placements, task.exclusion_level)
        if not exclusion_specification:
            with specification.uow as uow:
                for placement in placements:
                    is_allowlisted = False
                    if uow.allowlisting.get_by_conditions({
                            "name":
                            placement.placement,
                            "type":
                            placement.placement_type,
                            "account_id":
                            placement.customer_id
                    }):
                        is_allowlisted = True
                    placement["reason"] = ""
                    placement["allowlist"] = is_allowlisted
                reports.append(placements)
            continue
        for rule in exclusion_specification:
            # Identify all ads and non_ads specifications
            ads_specs = [
                r for r in rule
                if r.exclusion_type == ExclusionTypeEnum.GOOGLE_ADS_INFO
            ]
            non_ads_specs = [
                r for r in rule
                if r.exclusion_type != ExclusionTypeEnum.GOOGLE_ADS_INFO
            ]

            # If we don't have any non_ads specification proceed to applying them
            if ads_specs and not non_ads_specs:
                continue
            # If we have a mix of ads and non_ads specifications apply ads first
            # and then parse non-ads ones
            elif ads_specs and non_ads_specs:
                to_be_parsed_placements = (specification.apply_specifications(
                    [ads_specs], placements))
                parse_via_external_parsers(to_be_parsed_placements,
                                           non_ads_specs, specification.uow,
                                           save_to_db)
            # If there are only non_ads specification proceed to applying them
            elif not ads_specs and non_ads_specs:
                parse_via_external_parsers(placements, non_ads_specs,
                                           specification.uow, save_to_db)

        if (to_be_excluded_placements :=
                specification.apply_specifications(exclusion_specification,
                                                   placements)):
            reports.append(to_be_excluded_placements)
    if reports:
        return reduce(add, reports)
    return None


def parse_via_external_parsers(
    to_be_parsed_placements: GaarfReport,
    non_ads_specs: Sequence[BaseExclusionSpecification],
    uow: unit_of_work.AbstractUnitOfWork,
    save_to_db: bool = True,
    batch_size: int = 50,
) -> None:
    with uow:
        for non_ads_spec_rule in non_ads_specs:
            repo = getattr(uow, non_ads_spec_rule.repository_name)
            not_parsed_placements = []
            for placement_info in to_be_parsed_placements:
                if (placement_info.placement_type ==
                        non_ads_spec_rule.corresponding_placement_type.name):

                    if not repo.get_by_conditions({
                            "placement":
                            placement_info.placement,
                            # TODO (amarkin): reprocess placements that weren't process last time
                            # "is_processed": 1
                    }):
                        not_parsed_placements.append(
                            str(placement_info.placement))

            if not_parsed_placements:
                i = 0
                while batch := list(
                        itertools.islice(not_parsed_placements, i,
                                         i + batch_size)):
                    parsed_placements_info = non_ads_spec_rule.parser().parse(
                        batch)
                    i += batch_size
                    if save_to_db:
                        logging.debug(
                            f"saving placement: {placement_info.placement} to db"
                        )
                        for parsed_placement in parsed_placements_info:
                            repo.add(parsed_placement)
                        uow.commit()


def save_task(
    cmd: commands.SaveTask,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    with uow:
        task_id = None
        task_obj = None
        if hasattr(cmd, "task_id") and cmd.task_id:
            task_id = cmd.task_id
            task_obj = uow.tasks.get(task_id=task_id)
            update_dict = asdict(cmd)
            update_dict.pop("task_id")
            uow.tasks.update(task_obj.id, update_dict)
            if cmd.schedule:
                uow.published_events.append(
                    events.TaskUpdated(cmd.task_id, cmd.schedule))
            else:
                uow.published_events.append(events.TaskDeleted(cmd.task_id))
        else:
            task_dict = asdict(cmd)
            task_dict.pop("task_id")
            task_obj = task.Task(**task_dict)
            uow.tasks.add(task_obj)
            task_id = task_obj.id
            if cmd.schedule:
                uow.published_events.append(
                    events.TaskCreated(task_id, cmd.name, cmd.schedule))
        uow.commit()
        task_id = task_obj.id
        return str(task_id)


def delete_task(
    cmd: commands.DeleteTask,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        task_obj = uow.tasks.get(task_id=cmd.task_id)
        if task_obj:
            uow.tasks.update(cmd.task_id, {"status": "INACTIVE"})
            uow.commit()
            uow.published_events.append(events.TaskDeleted(cmd.task_id))
        else:
            logging.warning("No task with id %d found!", cmd.id)


def save_config(
    cmd: commands.SaveConfig,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        task_id = None
        task_obj = None
        if hasattr(cmd, "id") and cmd.id:
            config_id = cmd.id
            config = uow.settings.get(config_id)
            update_dict = asdict(cmd)
            update_dict.pop("id")
            uow.settings.update(config.id, update_dict)
        else:
            config_dict = asdict(cmd)
            config_dict.pop("id")
            config = settings.Config(**config_dict)
            uow.settings.add(config)
        uow.commit()


def add_to_allowlisting(cmd: commands.AddToAllowlisting,
                        uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        if not uow.allowlisting.get_by_conditions(asdict(cmd)):
            placement = allowlisting.AllowlistedPlacement(**asdict(cmd))
            uow.allowlisting.add(placement)
            uow.commit()


def remove_from_allowlisting(cmd: commands.RemoveFromAllowlisting,
                             uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        if allowlisted_placement := uow.allowlisting.get_by_conditions(
                asdict(cmd)):
            uow.allowlisting.delete(allowlisted_placement[0].id)
            uow.commit()


def save_channel_info(cmd: commands.SaveChannelInfo,
                      uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        uow.youtube_channel_info.add(cmd.channel_info)
        uow.commit()


def save_video_info(cmd: commands.SaveChannelInfo,
                    uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        uow.youtube_video_info.add(cmd.video_info)
        uow.commit()


def save_website_info(cmd: commands.SaveChannelInfo,
                      uow: unit_of_work.AbstractUnitOfWork) -> None:
    with uow:
        uow.website_info.add(cmd.website_info)
        uow.commit()


EVENT_HANDLERS = {
    events.TaskCreated: [task_created],
    events.TaskUpdated: [task_updated],
    events.TaskDeleted: [task_deleted]
}

COMMAND_HANDLERS = {
    commands.RunTask: run_task,
    commands.SaveTask: save_task,
    commands.DeleteTask: delete_task,
    commands.RunManualExclusion: run_manual_exclusion_task,
    commands.PreviewPlacements: preview_placements,
    commands.SaveConfig: save_config,
    commands.GetCustomerIds: get_customer_ids,
    commands.GetMccIds: get_accessible_mcc_ids,
    commands.AddToAllowlisting: add_to_allowlisting,
    commands.RemoveFromAllowlisting: remove_from_allowlisting,
    commands.SaveChannelInfo: save_channel_info,
    commands.SaveVideoInfo: save_video_info,
    commands.SaveWebsiteInfo: save_website_info,
}
