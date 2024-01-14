# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generic
from typing import TypeVar

import pydantic


__all__: list[str] = [
    'ResourceKey'
]

T = TypeVar('T')


class ResourceKey(pydantic.BaseModel, Generic[T]):
    api_version: str
    kind: str
    name: T