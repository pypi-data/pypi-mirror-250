# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from canonical.ext.iam import BaseAuthorizationContext
from canonical.ext.iam.types import PermissionSet
from canonical.ext.resource import ResourceType
from ..resourceclient import ResourceClient
from .impersonationauth import ImpersonationAuth
from .requestemail import RequestEmail
from .resourcerepository import ResourceRepository


__all__: list[str] = [
    'RemoteAuthorizationContext'
]


class RemoteAuthorizationContext(BaseAuthorizationContext):
    model: type[ResourceType]
    verb: str

    @property
    def client(self) -> ResourceClient:
        return ResourceClient(
            auth=self.auth,
            base_url='https://core.molanoapis.com'
        )

    def __init__(
        self,
        request: fastapi.Request,
        auth: ImpersonationAuth,
        resources: ResourceRepository,
        email: RequestEmail,
    ):
        self.auth = auth
        self.email = email
        self.granted = PermissionSet()
        self.repo = resources
        self.request = request
        self.subject_type = 'User'

    async def setup(self):
        self.model: type[ResourceType] = getattr(self.request.state, 'model')
        self.namespace: str | None = getattr(self.request.state, 'namespace', None)
        self.verb: str = getattr(self.request.state, 'verb')
        self.api_group = self.model.group
        self.plural = self.model.plural
        self.permission = self.get_permission_name(self.api_group, self.plural, self.verb)
        if not self.namespace:
            return