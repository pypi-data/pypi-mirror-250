# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Iterable

from .protocols import IResourceAuthorizationContext


class BaseAuthorizationContext(IResourceAuthorizationContext):

    def is_authenticated(self) -> bool:
        return False

    def is_authorized(self) -> bool:
        return False

    def has_permissions(self, permissions: Iterable[str]) -> set[str]:
        raise NotImplementedError

    async def get_permissions(self, permissions: set[str]) -> set[str]:
        raise NotImplementedError

    async def setup(self):
        pass

    async def _setup(self):
        await self.setup()
        return self

    def __await__(self):
        return self._setup().__await__()