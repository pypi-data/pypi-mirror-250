# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import cast
from typing import get_args
from typing import get_origin
from typing import Any
from typing import Callable
from typing import Generic
from typing import TypeVar
from typing import Union

import fastapi
import fastapi.params
from fastapi.exceptions import HTTPException

from canonical.ext.jsonpatch import JSONPatchType
from canonical.ext.iam import PermissionQuery
from canonical.ext.iam import PermissionSet
from canonical.ext.resource import Error
from canonical.ext.resource import Resource
from canonical.ext.resource import RootResource
from canonical.utils import merge_signatures
from .apiroute import APIRoute
from .params import AcceptedContentType
from .params import NegotiateResponseMediaType
from .params import RequestAuthorizationContext
from .params import RequestResource
from .params import RequestVerb
from .params import ResourceRepository
from .resourceoptions import ResourceOptions
from .response import Response


R = TypeVar('R', bound=Resource[Any] | RootResource[Any])
ResponseModel = TypeVar('ResponseModel')


class ResourceRouter(fastapi.APIRouter, Generic[R]):
    detail_verbs: set[str] = {
        'authorize',
        'destroy',
        'exists',
        'get',
        'inspect',
        'replace',
        'update',
    }
    response_class: type[Response[R]]
    resource_model: type[R]

    def __init__(
        self,
        *,
        model: type[R],
        register_resource: Callable[[str, type[R]], None],
        tags: list[dict[str, Any]],
        authorization: fastapi.params.Depends,
        **kwargs: Any
    ):
        deps: list[Any] = kwargs.setdefault('dependencies', [])
        deps.extend([
            NegotiateResponseMediaType({
                'text/html',
                'application/yaml',
                'application/json'
            }),
            fastapi.Depends(self.inject_namespace),
            fastapi.Depends(self.inject_model),
        ])
        self.authorization = authorization
        self.register_resource = register_resource
        responses = kwargs.pop('responses', {})
        responses.update({
            401: {
                'model': Error,
                'description': (
                    "Authentication is required to perform the requested "
                    "operation or the provided credential is invalid."
                )
            },
            403: {
                'model': Error,
                'description': (
                    "Untrusted credential or the authenticated request is not allowed "
                    "to perform the requested operation."
                )
            },
            406: {
                'model': Error,
                'description': (
                    "The media type accepted by the client can not be "
                    "satisfied by the server."
                )
            },
            500: {
                'model': Error,
                'description': (
                    "The server encountered an unexpected condition that "
                    "prevented it from fulfilling the request."
                )
            }
        })

        detail_responses = {
            404: {
                'model': Error,
                'description': (
                    f'The {model.__name__} specified by the path parameter(s) '
                    'does not exist.'
                )
            }
        }

        write_responses = {
            415: {
                'model': Error,
                'description': "Invalid content type for request body."
            },
        }

        super().__init__(
            responses=responses,
            route_class=APIRoute,
            **kwargs
        )
        self.response_class = Response.typed(model)
        self.resource_model = model
        self.add_api_route(
            methods=['POST'],
            path=f'/{model.base_path}',
            endpoint=self.writer_factory(self.resource_model, self.create),
            summary=f'Create endpoint',
            description=f"Create a `{model.__name__}` object.",
            dependencies=[
                AcceptedContentType({'application/yaml', 'application/json'}),
                fastapi.Depends(self.set_verb('create'))
            ],
            response_model=model,
            status_code=201,
            responses={
                **write_responses,
                409: {
                    'model': Error,
                    'description': (
                        f'A {model.__name__} with an identical '
                        'key exists.'
                    )
                }
            },
            response_description=f"{model.__name__} object.",
            response_model_by_alias=True,
            tags=[model.__name__]
        )

        self.add_resource_route(
            method='GET',
            verb='get',
            detail=True,
            path=f'/{model.base_path}/{{name}}',
            endpoint=self.retrieve,
            summary=f'Retrieve endpoint',
            description=f"Retrieve a `{model.__name__}` object.",
            response_model=model,
            responses={**detail_responses},
            response_description=f"{model.__name__} object.",
        )

        self.add_api_route(
            methods=['PUT'],
            path=f'/{model.base_path}/{{name}}',
            endpoint=self.writer_factory(self.resource_model, self.replace),
            summary=f'Replace endpoint',
            description=f"Replace a `{model.__name__}` object.",
            dependencies=[
                AcceptedContentType({'application/yaml', 'application/json'}),
                fastapi.Depends(self.set_verb('replace'))
            ],
            response_model=model,
            status_code=205,
            responses={
                **detail_responses,
                **write_responses,
                409: {
                    'model': Error,
                    'description': (
                        f'The {model.__name__} identified by the path parameters '
                        'can not be replaced.'
                    )
                }
            },
            response_description=f"{model.__name__} object.",
            response_model_by_alias=True,
            tags=[model.__name__]
        )

        self.add_api_route(
            methods=['PATCH'],
            path=f'/{model.base_path}/{{name}}',
            endpoint=self.update,
            summary=f'Update endpoint',
            description=f"Update a `{model.__name__}` object.",
            dependencies=[
                AcceptedContentType({'application/yaml', 'application/json'}),
                fastapi.Depends(self.set_verb('update'))
            ],
            response_model=model,
            status_code=205,
            responses={
                **detail_responses,
                **write_responses,
                409: {
                    'model': Error,
                    'description': (
                        f'One or more of the patches can not be applied to the {model.__name__}.'
                    )
                }
            },
            response_description=f"Updated {model.__name__} object.",
            response_model_by_alias=True,
            tags=[model.__name__]
        )

        if model.is_destroyable():
            self.add_api_route(
                methods=['DELETE'],
                path=f'/{model.base_path}/{{name}}',
                endpoint=self.destroy,
                summary=f'Destroy endpoint',
                description=f"Destroy a `{model.__name__}` object.",
                dependencies=[
                    fastapi.Depends(self.set_verb('destroy'))
                ],
                response_model=model,
                status_code=200,
                responses={
                    **detail_responses,
                    409: {
                        'model': Error,
                        'description': (
                            f'The {model.__name__} identified by the path parameters '
                            'can not be destroyed.'
                        )
                    }
                },
                response_description=f"Last version of the {model.__name__} object.",
                response_model_by_alias=True,
                tags=[model.__name__]
            )

        self.add_resource_route(
            method='GET',
            verb='list',
            path=f'/{model.base_path}',
            endpoint=self.collection,
            summary=f'List endpoint',
            description=f"Retrieve a list of `{self.resource_model.List.__name__}` objects.",
            response_model=model.List,
            response_description=f"{model.List.__name__} object.",
        )

        self.add_resource_route(
            method='POST',
            verb='authorize',
            detail=True,
            path=f'/{model.base_path}/{{name}}:permissions',
            endpoint=self.permissions,
            summary=f'Permissions endpoint',
            description=(
                f"Get the permissions granted to the authenticated "
                f"subject on a specific `{model.__name__}` object."
            ),
            response_model=PermissionSet,
            response_description=f"PermissionSet object.",
            responses={
                401: {
                    'model': Error,
                    'description': (
                        "The provided request credential is expired, not effective"
                        ", or otherwise malformed."
                    )
                },
                403: {
                    'model': Error,
                    'description': "Untrusted credential."
                },
            },
            authenticated=False
        )
        if model.is_purgable():
            self.add_api_route(
                methods=['DELETE'],
                path=f'/{model.base_path}',
                endpoint=self.purge,
                summary=f'Purge endpoint',
                description=f"Purge a collection of `{model.__name__}` objects.",
                dependencies=[
                    fastapi.Depends(self.set_verb('destroy'))
                ],
                response_model=model,
                status_code=202,
                responses={
                    409: {
                        'model': Error,
                        'description': (
                            f'The {model.List.__name__} identified by the path parameters '
                            'can not be purged.'
                        )
                    }
                },
                response_description=f"No content.",
                response_model_by_alias=True,
                tags=[model.__name__]
            )

        self.add_resource_route(
            method='OPTIONS',
            verb='inspect',
            detail=True,
            path=f'/{model.base_path}/{{name}}',
            endpoint=self.inspect,
            summary=f'{model.__name__} metadata',
            description=f"Retrieve metadata describing the resource type.",
            responses={
                200: {
                    'model': ResourceOptions,
                    'headers': {
                        'Accept': {
                            'description': (
                                "A comma-separated list describing the allowed "
                                "HTTP methods on this endpoint."
                            )
                        }
                    }
                },
                401: {
                    'model': Error,
                    'description': (
                        "The provided request credential is expired, not effective"
                        ", or otherwise malformed."
                    )
                },
                403: {
                    'model': Error,
                    'description': "Untrusted credential."
                },
            },
            response_description=f"ResourceOptions object.",
            response_model=ResourceOptions,
        )

        tags.append({
            'name': model.__name__,
            'description': getattr(model, '__doc__', None)
        })

    @classmethod
    def with_model(cls, model: type[R], **kwargs: Any) -> 'ResourceRouter[R]':
        models: tuple[type[Resource[Any]] | type[RootResource[Any]], ...] = tuple([])
        if get_origin(model) == Union:
            models = get_args(model)
        if not models:
            return cls(model=model, **kwargs)
        router = fastapi.APIRouter()
        for m in models: # type: ignore
            router.include_router(router=cls(model=m, **kwargs))
        return cast(ResourceRouter[model], router)

    def add_resource_route(
        self,
        *,
        verb: str,
        method: str,
        path: str,
        summary: str,
        description: str,
        endpoint: Any,
        response_model: type[Any] | None = None,
        response_description: str,
        responses: dict[int, Any] | None = None,
        dependencies: list[Any] | None = None,
        detail: bool = False,
        authenticated: bool = True
    ) -> None:
        model = self.resource_model
        responses = dict(responses or {})
        dependencies = dependencies or []
        if verb in self.detail_verbs:
            detail = True
        if verb in {'create', 'replace', 'update', 'authorize'}:
            dependencies.append(AcceptedContentType({'application/yaml', 'application/json'}))
            responses.update({
                415: {
                    'model': Error,
                    'description': "Invalid content type for request body."
                },
            })
        if detail:
            responses.update({
                404: {
                    'model': Error,
                    'description': (
                        f'The {model.__name__} specified by the path parameter(s) '
                        'does not exist.'
                    )
                }
            })
            dependencies.insert(0, self.inject_resource())
        if not authenticated:
            responses.pop(401, None)
        self.add_api_route(
            methods=[method],
            path=path,
            endpoint=endpoint,
            summary=summary,
            description=description,
            responses={**responses},
            response_model=self.resource_model or response_model,
            response_model_by_alias=True,
            response_description=response_description,
            dependencies=[
                fastapi.Depends(self.set_verb(verb)),
                *dependencies,
                self.authorization,
                fastapi.Depends(self.authorize),
            ],
            tags=[model.__name__],
        )
        self.register_resource(path, self.resource_model)

    def get_media_type(self, request: fastapi.Request) -> str:
        return getattr(request.state, 'media_type')

    def inject_model(self, request: fastapi.Request):
        setattr(request.state, 'model', self.resource_model)

    def inject_namespace(self, request: fastapi.Request):
        if 'name' in request.path_params:
            setattr(request.state, 'name', request.path_params['name'])
        if 'namespace' in request.path_params:
            setattr(request.state, 'namespace', request.path_params['namespace'])

    def inject_resource(self):
        return self._inject_resource_namespaced()\
            if self.resource_model.is_namespaced()\
            else self._inject_resource_cluster()

    def writer_factory(self, model: type[R], func: Any, partial: bool = False):
        async def f(resource: model, *args: Any, **kwargs: Any) -> Any:
            return await func(resource, *args, **kwargs)
        f.__signature__ = merge_signatures([ # type: ignore
            inspect.signature(func),
            inspect.signature(f)
        ])
        return f

    def set_verb(self, verb: str):
        def f(request: fastapi.Request):
            setattr(request.state, 'verb', verb)
        return f

    async def authorize(
        self,
        ctx: RequestAuthorizationContext,
        verb: RequestVerb
    ) -> None:
        if verb == 'authorize':
            return
        if not ctx.is_authenticated():
            raise HTTPException(
                status_code=401,
                detail="Authentication required."
            )
        if not ctx.is_authorized():
            raise HTTPException(
                status_code=403,
                detail=(
                    "The request subject is not granted permission "
                    "to perform this operation."
                )
            )

    async def collection(self) -> Resource[Any]:
        raise NotImplementedError

    async def create(self, resource: R) -> Resource[Any]:
        raise NotImplementedError

    async def destroy(self) -> Resource[Any]:
        raise NotImplementedError

    async def permissions(
        self,
        request: fastapi.Request,
        ctx: RequestAuthorizationContext,
        query: PermissionQuery
    ) -> Response[Any]:
        return self.render_to_response(
            request=request,
            status_code=200,
            instance=PermissionSet(
                granted=await ctx.get_permissions({str(p) for p in query.spec.permissions})
            )
        )

    async def purge(self) -> Resource[Any]:
        raise NotImplementedError

    async def replace(self, resource: R) -> Resource[Any]:
        raise NotImplementedError

    async def retrieve(
        self,
        request: fastapi.Request,
        resource: RequestResource,
    ) -> Response[Any]:
        return self.render_to_response(
            request=request,
            status_code=200,
            instance=resource
        )

    def render_to_response(self, *, request: fastapi.Request, instance: Any, status_code: int = 200) -> Response[Any]:
        return Response(
            status_code=status_code,
            media_type=self.get_media_type(request),
            content=instance
        )

    async def update(
        self,
        patch: JSONPatchType,
        name: str = fastapi.Path(...)
    ) -> Resource[Any]:
        raise NotImplementedError

    async def inspect(self) -> ResourceOptions:
        raise NotImplementedError

    def _inject_resource_cluster(self) -> Any:
        async def f(
            request: fastapi.Request,
            repo: ResourceRepository,
            name: str = fastapi.Path(
                description=f'The `.metadata.name` of an existing {self.resource_model.__name__}.',
                max_length=64,
            )
        ):
            try:
                resource = await repo.get_by_name(self.resource_model, name)
                setattr(request.state, 'resource', resource)
            except repo.DoesNotExist:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"The {self.resource_model.__name__} specified by "
                        f"the path parameters does not exist: '{name}'."
                    )
                )

        return fastapi.Depends(f)

    def _inject_resource_namespaced(self) -> Any:
        async def f(
            repo: ResourceRepository,
            request: fastapi.Request,
            namespace: str = fastapi.Path(
                description=(
                    "Identifies the namespace that contains the "
                    f"`{self.resource_model.__name__}`."
                )
            ),
            name: str = fastapi.Path(
                description=(
                    f'The `.metadata.name` of an existing '
                    f'`{self.resource_model.__name__}`.'
                )
            )
        ):
            try:
                resource = await repo.get_by_name(self.resource_model, name, namespace=namespace)
                setattr(request.state, 'resource', resource)
            except repo.DoesNotExist:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"The {self.resource_model.__name__} specified by "
                        f"the path parameters does not exist: '{name}'."
                    )
                )

        return fastapi.Depends(f)