# Copyright (C) 2023 Cochise Ruhulessin
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

from ..resourceid import ResourceID


N = TypeVar('N')
T = TypeVar('T')


class NamespaceSpec(pydantic.BaseModel):
    finalizers: set[str] = pydantic.Field(
        default_factory=list,
        description=(
            "Finalizers is an opaque list of values that must "
            "be empty to permanently remove object from storage."
        )
    )


class HierarchicalNamespaceSpec(NamespaceSpec, Generic[N, T]):
    parent: ResourceID[N, T] | None = pydantic.Field(
        default=None,
        description=(
            "An optional reference to a parent Resource.\n\nSupported parent "
            "types include `organization` and `folder`. Once set, the parent "
            "cannot be cleared. The parent can be set on creation or "
            "using the `projects.update` method; the end user must "
            "have the `projects.create` permission on the parent."
        )
    )