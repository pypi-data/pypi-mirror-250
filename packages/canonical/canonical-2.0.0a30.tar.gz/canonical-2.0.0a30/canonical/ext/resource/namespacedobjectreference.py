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

from .objectreference import ObjectReference


__all__: list[str] = [
    'NamespacedObjectReference'
]

G = TypeVar('G')
N = TypeVar('N')
K = TypeVar('K')
T = TypeVar('T')


class NamespacedObjectReference(ObjectReference[G, K, T], Generic[G, K, T, N]):
    model_config = {'populate_by_name': True}

    namespace: N = pydantic.Field(
        default=...,
        description=(
            "The `.metadata.namespace` of of the referent. Cannot be "
            "updated."
        ),
        frozen=True
    )