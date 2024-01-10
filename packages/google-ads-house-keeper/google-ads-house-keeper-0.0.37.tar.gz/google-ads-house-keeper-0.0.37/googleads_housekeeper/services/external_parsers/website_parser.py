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

import aiohttp
import asyncio
from collections.abc import Sequence
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import uuid

from .base_parser import BaseParser


@dataclass
class WebsiteInfo:
    placement: str
    title: str = ""
    description: str = ""
    keywords: str = ""
    is_processed: bool = False
    last_processed_time: datetime = datetime.now()
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class WebSiteParser(BaseParser):

    def parse(self, placements: Sequence[str]) -> list[WebsiteInfo]:
        return asyncio.run(self._parse_placements(placements))

    async def _parse_placements(
            self, placements: Sequence[str]) -> list[WebsiteInfo]:
        timeout = aiohttp.ClientTimeout(total=1)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            results = []
            for placement in placements:
                results.append(self._parse_placement(placement, session))
            values = await asyncio.gather(*results)
        return values

    async def _parse_placement(self, placement: str,
                               session: aiohttp.ClientSession) -> WebsiteInfo:
        url = self._convert_placement_to_url(placement)
        try:
            html = await self._fetch_html(url, session)
            placement_info  = await self._extract_from_html(placement, html)
            return placement_info
        except Exception as e:
            return WebsiteInfo(placement=placement)

    def _convert_placement_to_url(self, placement: str) -> str:
        if "http" not in placement:
            https = "https://"
            url = f"https://{placement}"
        else:
            url = placement
        return url

    async def _fetch_html(self, url: str, session: aiohttp.ClientSession):
        response = await session.request(method="GET", url=url)
        response.raise_for_status()
        html = await response.text()
        return html

    async def _extract_from_html(self, url: str, html: str) -> WebsiteInfo:
        soup = BeautifulSoup(html, 'html.parser')
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        description = soup.find('meta', attrs={'name': 'description'})
        return WebsiteInfo(
            placement=url,
            title=soup.title.string if soup.title else None,
            keywords=keywords.get("content") if keywords else None,
            description=description.get("content") if description else None,
            is_processed=True)
