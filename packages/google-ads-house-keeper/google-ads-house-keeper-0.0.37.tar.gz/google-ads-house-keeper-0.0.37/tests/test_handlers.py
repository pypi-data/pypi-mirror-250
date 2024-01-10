from typing import List

from collections import defaultdict
from datetime import datetime
from googleads_housekeeper import bootstrap, views
from googleads_housekeeper.adapters import repository, notifications, publisher
from googleads_housekeeper.domain import commands, events, task
from googleads_housekeeper.services import enums, external_parsers, unit_of_work
import pytest


class TestTask:

    def test_create_task_populated_repository(self, bus):
        cmd = commands.SaveTask(exclusion_rule="clicks > 0", customer_ids="1")
        bus.handle(cmd)
        assert bus.uow.tasks.list()

    def test_create_task_publish_task_create_event(self, bus, fake_publisher):
        cmd = commands.SaveTask(exclusion_rule="clicks > 0", customer_ids="1")
        bus.handle(cmd)
        assert isinstance(fake_publisher.events[0], events.TaskCreated)

    def test_create_task_process_queue(self, bus):
        cmd = commands.SaveTask(exclusion_rule="clicks > 0", customer_ids="1")
        bus.handle(cmd)
        assert not bus.queue

    def test_tasks_view_is_not_empty_after_creating_task(self, bus):
        cmd = commands.SaveTask(exclusion_rule="clicks > 0", customer_ids="1")
        bus.handle(cmd)
        assert views.tasks(bus.uow)

    def test_update_task_change_task_in_repository(self, bus):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        update_cmd = commands.SaveTask(exclusion_rule="clicks > 1",
                                       customer_ids="2",
                                       task_id=task_id)
        bus.handle(update_cmd)
        assert bus.uow.tasks.get(task_id).exclusion_rule == "clicks > 1"
        assert bus.uow.tasks.get(task_id).customer_ids == "2"

    def test_update_task_publish_task_updated_event(self, bus, fake_publisher):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        update_cmd = commands.SaveTask(exclusion_rule="clicks > 1",
                                       customer_ids="2",
                                       task_id=task_id)
        bus.handle(update_cmd)
        assert events.TaskCreated(task_id) in fake_publisher.events
        assert events.TaskUpdated(task_id) in fake_publisher.events

    def test_update_task_process_queue(self, bus):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        update_cmd = commands.SaveTask(exclusion_rule="clicks > 1",
                                       customer_ids="2",
                                       task_id=task_id)
        bus.handle(update_cmd)
        assert not bus.queue

    def test_delete_task_makes_task_status_inactive(self, bus):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        delete_cmd = commands.DeleteTask(task_id=task_id)
        bus.handle(delete_cmd)
        assert bus.uow.tasks.get(task_id).status == task.TaskStatus.INACTIVE

    def test_delete_task_publishes_task_deleted_event(self, bus,
                                                      fake_publisher):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        delete_cmd = commands.DeleteTask(task_id=task_id)
        bus.handle(delete_cmd)
        assert events.TaskCreated(task_id) in fake_publisher.events
        assert events.TaskDeleted(task_id) in fake_publisher.events

    def test_delete_task_process_queue(self, bus, fake_publisher):
        create_cmd = commands.SaveTask(exclusion_rule="clicks > 0",
                                       customer_ids="1")
        task_id = bus.handle(create_cmd)
        delete_cmd = commands.DeleteTask(task_id=task_id)
        bus.handle(delete_cmd)
        assert not bus.queue


class TestAllowlisting:

    def test_add_to_allowlisting_create_entry_in_repository(self, bus):
        allowlisting_cmd = commands.AddToAllowlisting(
            type=enums.PlacementTypeEnum.MOBILE_APPLICATION,
            name="fake_name",
            account_id="1")
        bus.handle(allowlisting_cmd)
        assert bus.uow.allowlisting.list()

    def test_remove_from_allowlisting_empties_in_repository(self, bus):
        allowlisting_cmd = commands.AddToAllowlisting(
            type=enums.PlacementTypeEnum.MOBILE_APPLICATION,
            name="fake_name",
            account_id="1")
        bus.handle(allowlisting_cmd)
        removal_allowlisting_cmd = commands.RemoveFromAllowlisting(
            type=enums.PlacementTypeEnum.MOBILE_APPLICATION,
            name="fake_name",
            account_id="1")
        bus.handle(removal_allowlisting_cmd)
        assert not bus.uow.allowlisting.list()
