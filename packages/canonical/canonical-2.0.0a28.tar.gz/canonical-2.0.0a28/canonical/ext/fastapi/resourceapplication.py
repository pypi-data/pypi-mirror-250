# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi

from canonical.ext.resource import Error
from canonical.ext.resource import Resource
from canonical.ext.resource import ResourceType
from canonical.ext.resource import RootResource
from canonical.utils.http import MediaTypeSelector

from .resourcerouter import ResourceRouter
from .response import Response


class ResourceApplication(fastapi.FastAPI):
    resource_paths: set[str] = set()
    media_types: MediaTypeSelector = MediaTypeSelector({
        'text/html',
        'application/json',
        'application/yaml'
    })

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        @self.exception_handler(404)
        def _(request: fastapi.Request, _: Any) -> Any:
            assert request.client is not None
            return Response(
                media_type=self.media_types.select(request.headers.get('Accept')),
                status_code=404,
                content=Error.factory({
                    'status_code': 404,
                    'detail': "The server cannot find the requested resource",
                    'request': {
                        'url': str(request.url),
                        'host': request.client.host
                    }
                })
            )

    def add(self, model: type[Resource[Any] | RootResource[Any]], **kwargs: Any):
        self.openapi_tags = self.openapi_tags or []
        self.include_router(
            router=ResourceRouter.with_model(
                model=model,
                register_resource=self.register_resource,
                tags=self.openapi_tags,
                **kwargs
            ),
        )

    def register_resource(self, path: str, _: ResourceType) -> None:
        self.resource_paths.add(path)