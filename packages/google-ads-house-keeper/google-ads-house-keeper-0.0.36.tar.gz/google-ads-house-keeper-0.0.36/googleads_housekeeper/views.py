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
from typing import Any, Dict, List, Optional
from dataclasses import asdict
from functools import lru_cache

from googleads_housekeeper.services import unit_of_work

registry = {}


def task(task_id: int,
         uow: unit_of_work.AbstractUnitOfWork) -> dict[str, Any] | None:
    with uow:
        if task := uow.tasks.get(task_id):
            return asdict(task)
        return None


def tasks(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]]:
    with uow:
        tasks: list[dict[str, Any]] = []
        for task in uow.tasks.list():
            task_dict = task.to_dict()
            task_dict["next_run"] = task.next_run
            accounts = customer_ids(uow, accounts=task.customer_ids.split(","))
            task_dict["accounts"] = list(
                set([a.get("account_name") for a in accounts]))
            if task_executions := executions(task.id, uow):
                for execution in sorted(task_executions,
                                        key=lambda x: x.get("end_time"),
                                        reverse=True):
                    task_dict["placements_excluded"] = execution.get(
                        "placements_excluded")
                    task_dict["last_run"] = execution.get("end_time").strftime(
                        "%Y-%m-%d %H-%M")
                    break
            else:
                task_dict["placements_excluded"] = None
            tasks.append(task_dict)
        return tasks


def config(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]]:
    with uow:
        return [asdict(c) for c in uow.settings.list()]


def allowlisted_placements(
        uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]] | None:
    with uow:
        if allowlisted_placements := uow.allowlisting.list():
            return [asdict(t) for t in allowlisted_placements]
    return None


def execution(execution_id: str,
              uow: unit_of_work.AbstractUnitOfWork) -> dict[str, Any] | None:
    with uow:
        if task_execution := uow.executions.get(execution_id):
            return asdict(task_execution)
    return None


def executions(
        task_id: str,
        uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, Any]] | None:
    with uow:
        if task_executions := uow.executions.get_by_condition("task", task_id):
            return [asdict(t) for t in task_executions]
    return None


def execution_details(
        task_id: str,
        execution_id: str,
        uow: unit_of_work.AbstractUnitOfWork,
        first_n_placements: int | None = None) -> list[dict[str, Any]] | None:
    with uow:
        if task_executions := uow.executions.get_by_condition("task", task_id):
            if execution_details := uow.execution_details.get_by_condition(
                    "execution_id", execution_id):
                results = [asdict(t) for t in execution_details]
                if first_n_placements and first_n_placements < len(results):
                    results = results[:first_n_placements]
                return results
    return None


def customer_ids(uow: unit_of_work.AbstractUnitOfWork,
                 mcc_id: str | None = None,
                 accounts: list[str] | None = None) -> list[dict[str, Any]]:
    with uow:
        if mcc_id:
            customer_ids = [
                asdict(r) for r in uow.customer_ids.list()
                if r.mcc_id == mcc_id
            ]
        elif accounts:
            customer_ids = [
                asdict(r) for r in uow.customer_ids.list() if r.id in accounts
            ]
        else:
            raise ValueError("Neither mcc_id nor accounts were provided")
        return customer_ids


def mcc_ids(uow: unit_of_work.AbstractUnitOfWork) -> list[dict[str, str]]:
    if mcc_ids := registry.get("mcc_ids"):
        return mcc_ids
    with uow:
        mcc_ids = [asdict(r) for r in uow.mcc_ids.list()]
        registry["mcc_ids"] = mcc_ids
        return mcc_ids
