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
from ..resourceclient import ResourceClient
from .impersonationauth import ImpersonationAuth
from .requestemail import RequestEmail
from .requestverb import RequestVerb
from .resourcemodel import ResourceModel
from .resourcerepository import ResourceRepository
from .requestnamespace import RequestNamespace


class AuthorizationContext(BaseAuthorizationContext):

    def __init__(
        self,
        client: ResourceClient,
        resources: ResourceRepository,
        model: ResourceModel,
        verb: RequestVerb,
        namespace: RequestNamespace,
        email: RequestEmail,
    ):
        self.client = client
        self.api_group = model.group
        self.email = email
        self.granted = PermissionSet()
        self.model = model
        self.namespace = namespace
        self.permission = f'{model.group}.{model.plural}.{verb}'
        if not model.group:
            self.permission = f'{model.plural}.{verb}'
        self.repo = resources
        self.resource = model.plural
        self.subject_type = 'User'
        self.verb = verb


def RemoteAuthorization(
    server_url: str
):
    async def f(
        auth: ImpersonationAuth,
        resources: ResourceRepository,
        model: ResourceModel,
        verb: RequestVerb,
        namespace: RequestNamespace,
        email: RequestEmail,
    ):
        async with ResourceClient(base_url=server_url, auth=auth) as client:
            yield await AuthorizationContext(client=client)

    return fastapi.Depends(f)