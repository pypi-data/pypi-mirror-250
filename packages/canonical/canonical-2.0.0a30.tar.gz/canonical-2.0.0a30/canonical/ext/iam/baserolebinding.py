# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Literal

import pydantic

from canonical.ext.resource import Resource
from canonical.ext.resource import ObjectMetaType
from .rolereference import RoleReference
from .subject import Subject


class BaseRoleBinding(
    Resource[ObjectMetaType],
    version='rolebindings.iam.webiam.io/v1'
):
    subjects: list[Subject] = pydantic.Field(
        default=...,
        description=(
            "Holds references to the objects the role applies to."
        ),
        min_length=1
    )

    role_ref: RoleReference[Literal['ClusterRole', 'Role']] = pydantic.Field(
        default=...,
        alias='roleRef',
        description=(
            "The `roleRef` property must reference a `Role` in the current namespace "
            "or a `GlobalRole` in the global namespace. If `roleRef` cannot be resolved, "
            "the Authorizer must return an error."
        )
    )

    def __init_subclass__(cls, *, kind: str | None = None, **kwargs: Any):
        if kind is not None:
            cls.model_fields['role_ref'].annotation = RoleReference[kind] # type: ignore
            cls.model_rebuild()
        super().__init_subclass__(**kwargs)

    def is_global(self) -> bool:
        return self.role_ref.is_global()