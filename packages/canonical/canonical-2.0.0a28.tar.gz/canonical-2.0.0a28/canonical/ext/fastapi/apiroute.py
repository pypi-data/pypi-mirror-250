# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any
from typing import Callable
from typing import Coroutine

import fastapi
import fastapi.routing
import starlette.responses
from fastapi.exceptions import HTTPException

from canonical.ext.resource import Error
from canonical.utils.http import MediaTypeSelector
from .response import Response


class APIRoute(fastapi.routing.APIRoute):
    logger: logging.Logger = logging.getLogger('uvicorn')
    media_types: MediaTypeSelector = MediaTypeSelector({
        'text/html',
        'application/json',
        'application/yaml'
    })

    def get_route_handler(self) -> Callable[[fastapi.Request], Coroutine[Any, Any, starlette.responses.Response]]:
        handler = super().get_route_handler()

        async def f(request: fastapi.Request) -> starlette.responses.Response:
            response: Response[Any]
            try:
                response = await handler(request) # type: ignore
            except HTTPException as e:
                assert request.client
                response = Response(
                    media_type=self.media_types.select(request.headers.get('Accept')),
                    status_code=e.status_code,
                    content=Error.factory({
                        'detail': e.detail,
                        'request': {
                            'url': str(request.url),
                            'host': request.client.host,
                        },
                        'status_code': e.status_code,
                    })
                )
            except Exception as e:
                self.logger.exception("Caught fatal exception.")
                assert request.client
                response = Response(
                    media_type=self.media_types.select(request.headers.get('Accept')),
                    status_code=500,
                    content=Error.factory({
                        'detail': (
                            "The server encountered an unexpected condition "
                            "that prevented it from fulfilling the request."
                        ),
                        'request': {
                            'url': str(request.url),
                            'host': request.client.host,
                        },
                        'status_code': 500,
                    })
                )
            return response
        return f