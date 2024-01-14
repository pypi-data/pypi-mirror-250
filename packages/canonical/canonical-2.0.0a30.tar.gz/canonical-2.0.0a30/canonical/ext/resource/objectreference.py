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
    'ObjectReference'
]

G = TypeVar('G')
K = TypeVar('K')
T = TypeVar('T')


class ObjectReference(pydantic.BaseModel, Generic[G, K, T]):
    model_config = {'populate_by_name': True}

    api_group: G = pydantic.Field(
        default=None,
        alias='apiGroup',
        title="API group",
        description=(
            "Specifies the API group of the referent. Cannot be updated."
        ),
        frozen=True
    )

    kind: K = pydantic.Field(
        default=...,
        description=(
            "Kind of the referent. Cannot be updated. In `CamelCase`."
        ),
        frozen=True
    )

    name: T = pydantic.Field(
        default=...,
        description=(
            "The `.metadata.name` of of the referent. Cannot be "
            "updated."
        ),
        frozen=True
    )