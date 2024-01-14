# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import logging
from typing import Any

import httpx


__all__: list[str] = [
    'AsyncClient',
]


class AsyncClient(httpx.AsyncClient):
    logger: logging.Logger = logging.getLogger('headless')

    @property
    def domain(self) -> str:
        return self.base_url.netloc.decode()

    def can_retry_timeout(self, request: httpx.Request):
        return request.method in {'GET', 'HEAD', 'OPTIONS'}

    async def request(self, *args: Any, **kwargs: Any) -> httpx.Response:
        attempts: int = 0
        delay: int = 5
        while True:
            attempts += 1
            must_log = attempts % 3 == 0
            try:
                response = await super().request(*args, **kwargs)
                response.raise_for_status()
                break
            except httpx.ConnectError as e:
                # Assumption is that there is no internet connection.
                if must_log:
                    self.logger.warning("Network issues prevent request (url: %s)", e.request.url)
                await asyncio.sleep(delay)
                continue
            except httpx.ConnectTimeout as e:
                # A connection timeout may occur due to intermediary issues, or
                # a booting application that has not bound its port yet.
                if must_log:
                    self.logger.warning("Connection timeout (url: %s)", e.request.url)
                await asyncio.sleep(delay)
                continue
            except httpx.ReadTimeout as e:
                # A read timeout means that we've succesfully connected, but there
                # was a timeout reading the response. This should only be retried on
                # safe HTTP methods, because we do not know what actually caused the
                # timeout, thus any destructive operations may actually have been
                # completed succesfully.
                if not self.can_retry_timeout(e.request):
                    raise
                await asyncio.sleep(delay)
                continue
            except httpx.HTTPStatusError as e:
                if e.response.status_code != 429:
                    response = e.response
                    break
                if must_log:
                    self.logger.warning("Request was rate-limited (url: %s)", e.response.url)
                await asyncio.sleep(delay)
        return response