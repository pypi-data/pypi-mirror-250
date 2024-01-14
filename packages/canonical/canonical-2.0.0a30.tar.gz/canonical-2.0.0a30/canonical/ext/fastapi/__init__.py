# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from canonical.ext.resource import IResourceRepository
from .resourceapplication import ResourceApplication
from .resourceclient import ResourceClient
from .resourcerouter import ResourceRouter


__all__: list[str] = [
    'ResourceApplication',
    'ResourceClient',
    'ResourceRouter'
]

def setup_dependencies(
    repository: type[IResourceRepository]
):
    async def f(
        request: fastapi.Request,
        resources: IResourceRepository = fastapi.Depends(repository)
    ):
        setattr(request.state, 'resources', resources)

    return [fastapi.Depends(f)]