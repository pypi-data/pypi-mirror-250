# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import overload
from typing import Any
from typing import NoReturn
from typing import TypeVar

import httpx
import pydantic
from fastapi.exceptions import HTTPException

from canonical.ext.iam import PermissionQuery
from canonical.ext.iam import PermissionSet
from canonical.ext.httpx import AsyncClient
from canonical.ext.resource import Error


T = TypeVar('T', bound=pydantic.BaseModel)


class ResourceClient(AsyncClient):

    def can_retry_timeout(self, request: httpx.Request):
        return super().can_retry_timeout(request) or any([
            str.endswith(request.url.path, ':permissions')
        ])

    def construct_uri(
        self,
        group: str,
        kind: str,
        name: str | None = None,
        namespace: str | None = None,
        version: str | None = None
    ):
        version = version or 'v1'
        url = f'{version}/{kind}'
        if group:
            url = f'{group}/{url}'
        if namespace is not None:
            url = f'/{group}/{version}/namespaces/{namespace}/{kind}'
        if name is not None:
            url = f'{url}/{name}'
        return url

    def raise_for_status(self, response: httpx.Response) -> NoReturn | None:
        if response.status_code >= 400:
            error = Error.model_validate_json(response.content)
            raise HTTPException(
                status_code=error.data.status_code,
                detail=error.data.detail
            )

    @overload
    def resource_factory(self, model: None, response: httpx.Response) -> dict[str, Any]:
        ...

    @overload
    def resource_factory(self, model: type[T], response: httpx.Response) -> T:
        ...

    def resource_factory(self, model: type[T] | None, response: httpx.Response) -> T | dict[str, Any]:
        return (
            response.json()
            if not model else
            model.model_validate_json(response.content)
        )

    async def permissions(
        self,
        namespace: str | None,
        permission: str,
        *permissions: str,
        **kwargs: Any
    ) -> set[str]:
        """Retrieve the permissions that the client has on the given
        resource.
        """
        query = PermissionQuery.factory({
            'permissions': {permission, *permissions}
        })
        if not kwargs:
            # Queries a namespace.
            response = await self.post(
                headers={
                    'Accept': 'application/json',
                },
                url=f"{self.construct_uri('', 'namespaces', namespace)}:permissions",
                json=query.model_dump(by_alias=True, mode='json')
            )
        else:
            raise NotImplementedError
        self.raise_for_status(response)
        result = PermissionSet.model_validate_json(response.content)
        return result.granted

        raise NotImplementedError
        response = await self.post(
            url=self.construct_uri(group, kind, name, namespace, version) + '/permissions',
            headers={'Accept': 'application/json'},
            json={
                'apiVersion': 'iam.webiam.io/v1',
                'kind': 'PermissionQuery',
                'spec': {
                    'permissions': [
                        'a.b.c',
                        'namespaces.list',
                        'namespaces.get',
                        'foo',
                        'bar',
                        'warehouse.rma.reject',
                        'warehouse.rma.list',
                    ]
                }
            }
        )
        self.raise_for_status(response)
        result = PermissionSet.model_validate_json(response.content)
        return result.granted

    @overload
    async def request_resource(self, model: None, **kwargs: Any) -> dict[str, Any]:
        ...

    @overload
    async def request_resource(self, model: type[T], **kwargs: Any) -> T:
        ...

    async def request_resource(self, model: type[T] | None, method: str, **kwargs: Any) -> T | dict[str, Any]:
        headers = kwargs.setdefault('headers', {})
        headers['Accept'] = 'application/json'
        response = await self.request(method=method, **kwargs)
        self.raise_for_status(response)
        resource = response.json()
        if model is not None:
            resource = self.resource_factory(model, response)
        return resource

    async def retrieve(
        self,
        group: str,
        kind: str,
        name: str,
        model: type[T] | None = None,
        namespace: str | None = None,
        version: str | None = None,
    ) -> dict[str, Any] | T:
        return await self.request_resource(
            model=model,
            method='GET',
            url=self.construct_uri(group, kind, name, namespace, version)
        )