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
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from googleapiclient.discovery import build
import uuid

from .base_parser import BaseParser


class YouTubeDataConnector:

    def __init__(self,
                 api_version: str = "v3",
                 developer_key: str = os.getenv("YOUTUBE_DATA_API_KEY")):
        self.service = build("youtube",
                             api_version,
                             developerKey=developer_key)

    def get_response(self, type_, elements, element_id):
        if type_ == "videos":
            service = self.service.videos()
        elif type_ == "channels":
            service = self.service.channels()
        else:
            raise ValueError(f"Unsupported resource {type_}")
        return service.list(part=elements, id=element_id).execute()


@dataclass
class ChannelInfo:
    placement: str
    title: str | None = None
    description: str | None = None
    country: str | None = None
    viewCount: int = 0
    subscriberCount: int = 0
    videoCount: int = 0
    topicCategories: str = ""
    last_processed_time: datetime = datetime.now()
    is_processed: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class VideoInfo:
    placement: str
    title: str | None = None
    description: str | None = None
    defaultLanguage: str | None = None
    defaultAudioLanguage: str | None = None
    commentCount: int = 0
    favouriteCount: int = 0
    likeCount: int = 0
    viewCount: int = 0
    madeForKids: bool = False
    tags: str = ""
    topicCategories: str = ""
    last_processed_time: datetime = datetime.now()
    is_processed: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class ChannelInfoParser(BaseParser):

    def __init__(self, data_connector=YouTubeDataConnector):
        self.data_connector = data_connector

    def parse(
        self,
        channel_ids: Sequence[str],
        elements: str = "id,snippet,statistics,topicDetails"
    ) -> list[ChannelInfo]:
        response = self.data_connector().get_response("channels", elements,
                                                      channel_ids)
        if not (items := response.get("items")):
            return [
                ChannelInfo(placement=channel_id, is_processed=False)
                for channel_id in channel_ids
            ]
        results: list[ChannelInfo] = []
        for item in items:
            if snippet := item.get("snippet"):
                title = snippet.get("title")
                description = snippet.get("description")
                country = snippet.get("country")
            else:
                title = None
                description = None
                country = None
            if statistics := item.get("statistics"):
                subscriberCount = safe_cast(int, statistics.get("subscriberCount"))
                viewCount = safe_cast(int, statistics.get("viewCount"))
                videoCount = safe_cast(int, statistics.get("videoCount"))
            else:
                subscriberCount = 0
                viewCount = 0
                videoCount = 0
            topics = parse_topic_details(item.get("topicDetails"))
            results.append(
                ChannelInfo(placement=item.get("id"),
                            title=title,
                            description=description,
                            country=country,
                            viewCount=viewCount,
                            subscriberCount=subscriberCount,
                            videoCount=videoCount,
                            topicCategories=topics))
        return results


class VideoInfoParser(BaseParser):

    def __init__(self, data_connector=YouTubeDataConnector):
        self.data_connector = data_connector

    def parse(
        self,
        video_ids: Sequence[str],
        elements:
        str = "id,status,snippet,statistics,contentDetails,topicDetails"
    ) -> list[VideoInfo]:
        response = self.data_connector().get_response("videos", elements,
                                                      video_ids)
        if not (items := response.get("items")):
            return [
                VideoInfo(placement=video_id, is_processed=False)
                for video_id in video_ids
            ]
        results: list[VideoInfo] = []
        for item in items:
            if snippet := item.get("snippet"):
                title = snippet.get("title")
                description = snippet.get("description")
                defaultLanguage = snippet.get("defaultLanguage")
                defaultAudioLanguage = snippet.get("defaultAudioLanguage")
                tags = snippet.get("tags")
            else:
                title = None
                description = None
                defaultLanguage = None
                defaultAudioLanguage = None
                tags = ""
            if statistics := item.get("statistics"):
                commentCount = safe_cast(int, statistics.get("commentCount"))
                favouriteCount = safe_cast(int, statistics.get("favouriteCount"))
                likeCount = safe_cast(int, statistics.get("likeCount"))
                viewCount = safe_cast(int, statistics.get("viewCount"))
            else:
                commentCount = 0
                favouriteCount = 0
                likeCount = 0
                viewCount = 0
            if status := item.get("status"):
                madeForKids = safe_cast(bool, status.get("madeForKids"))
            else:
                madeForKids = False
            topics = parse_topic_details(item.get("topicDetails"))
            if tags:
                tags = ",".join(tags)
            results.append(
                VideoInfo(placement=item.get("id"),
                          title=title,
                          description=description,
                          defaultLanguage=defaultLanguage,
                          defaultAudioLanguage=defaultAudioLanguage,
                          commentCount=commentCount,
                          favouriteCount=favouriteCount,
                          likeCount=likeCount,
                          viewCount=viewCount,
                          madeForKids=madeForKids,
                          tags=tags,
                          topicCategories=topics))
        return results


def parse_topic_details(topicDetails: Mapping[str, Any] | None) -> str:
    if not topicDetails:
        return ""
    if not (topic_categories := topicDetails.get("topicCategories")):
        return ""
    return ",".join(
        list(set([topic.split("/")[-1] for topic in topic_categories])))

def safe_cast(callable, value: str | None):
    if value:
        return callable(value)
    return callable()
