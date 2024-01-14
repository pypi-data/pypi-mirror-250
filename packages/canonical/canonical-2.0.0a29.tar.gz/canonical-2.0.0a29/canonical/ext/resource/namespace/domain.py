# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

import pydantic

from canonical import DomainName
from ..resourceid import ResourceID
from ..objectmeta import ObjectMeta
from .base import BaseNamespace
from .namespacespec import NamespaceSpec


class Domain(BaseNamespace[ObjectMeta[DomainName]], kind='Namespace', type='webiam.io/domain'):
    model_config = {'populate_by_name': True}

    spec: 'DomainSpec' = pydantic.Field(
        default_factory=NamespaceSpec,
        description="Defines the behavior of the `Namespace`."
    )


class DomainSpec(NamespaceSpec):
    parent: ResourceID[Literal['organization'], int] = pydantic.Field(
        default=...,
        description=(
            "Defines the organization the domain is verified for."
        )
    )


Domain.model_rebuild()