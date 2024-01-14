# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Iterable

import fastapi

from canonical.ext.iam import BaseAuthorizationContext
from canonical.ext.iam import ClusterRole
from canonical.ext.iam import ClusterRoleBinding
from canonical.ext.iam import Role
from canonical.ext.iam import RoleBinding
from canonical.ext.iam.types import PermissionSet
from canonical.ext.resource import Namespace
from .requestemail import RequestEmail
from .requestverb import RequestVerb
from .resourcemodel import ResourceModel
from .resourcerepository import ResourceRepository
from .requestnamespace import RequestNamespace
from .requestresource import RequestResource


class AuthorizationContext(BaseAuthorizationContext):
    logger: logging.Logger = logging.getLogger('uvicorn')
    roles: set[str]
    _cluster_roles: dict[str, ClusterRole] = NotImplemented
    _ready: bool = False

    def __init__(
        self,
        model: ResourceModel,
        repo: ResourceRepository,
        request: fastapi.Request,
        verb: RequestVerb,
        namespace: RequestNamespace,
        resource: RequestResource,
        email: RequestEmail,
    ):
        self._cluster_permissions = AuthorizationContext._cluster_roles
        self.api_group = model.group
        self.email = email
        self.granted = PermissionSet()
        self.model = model
        self.namespace = namespace
        self.permission = f'{model.group}.{model.plural}.{verb}'
        if not model.group:
            self.permission = f'{model.plural}.{verb}'
        self.repo = repo
        self.request = request
        self.resource = model.plural
        self.subject_type = 'User'
        self.verb = verb

        # Namespace is a special cause because permissions in the namespace
        # also apply to the namespace itself.
        if self.namespace is None and isinstance(resource, Namespace):
            self.namespace = resource.metadata.name

    def get_cluster_bindings(self):
        self.logger.debug(
            "Retrieving global role bindings (kind: %s, email: %s)",
            self.subject_type,
            self.email
        )
        return self.repo.query(
            model=ClusterRoleBinding,
            filters=[
                ('subjects.kind', '=', self.subject_type),
                ('subjects.name', '=', str(self.email)),
            ]
        )

    def get_namespace_bindings(self):
        self.logger.debug(
            "Retrieving local role bindings (namespace: %s, kind: %s, email: %s)",
            self.namespace,
            self.subject_type,
            self.email
        )
        return self.repo.query(
            model=RoleBinding,
            filters=[
                ('subjects.kind', '=', self.subject_type),
                ('subjects.name', '=', str(self.email)),
            ],
            namespace=self.namespace
        )

    def get_namespace_roles(self, roles: Iterable[str]):
        assert self.namespace is not None
        return self.repo.query(
            model=Role,
            filters=[('metadata.name', '=', list(roles))],
            namespace=self.namespace
        )

    def is_authenticated(self) -> bool:
        return self.email is not None

    def is_authorized(self) -> bool:
        return self.is_granted(self.permission)

    def is_granted(self, permission: str) -> bool:
        return self.granted.has(permission)

    async def get_permissions(self, permissions: set[str]) -> set[str]:
        return {p for p in permissions if self.is_granted(p)}

    async def get_namespace_permissions(self, roles: Iterable[str]) -> PermissionSet:
        permissions = PermissionSet()
        async for role in self.get_namespace_roles(roles):
            permissions.update(role.permissions)
        return permissions

    async def setup(self):
        await self.setup_cluster()

        scoped_roles: set[str] = set()
        global_roles: set[str] = set()
        async for binding in self.get_cluster_bindings():
            role = self._cluster_roles[binding.role_ref.name]
            self.granted.update(role.permissions)
        if self.namespace is not None:
            async for obj in self.get_namespace_bindings():
                if obj.is_global():
                    global_roles.add(obj.role_ref.name)
                else:
                    scoped_roles.add(obj.role_ref.name)

            self.granted |= await self.get_namespace_permissions(scoped_roles)

    async def setup_cluster(self):
        if self._cluster_roles != NotImplemented:
            return
        self.logger.debug("Retrieving cluster roles and permissions")
        self._cluster_roles = {}
        async for role in self.repo.all(ClusterRole):
            self._cluster_roles[role.metadata.name] = role


def LocalAuthorization():
    async def f(
        request: fastapi.Request,
        ctx: AuthorizationContext = fastapi.Depends(AuthorizationContext)
    ):
        setattr(request.state, 'resource_context', await ctx)
        return ctx
    return fastapi.Depends(f)