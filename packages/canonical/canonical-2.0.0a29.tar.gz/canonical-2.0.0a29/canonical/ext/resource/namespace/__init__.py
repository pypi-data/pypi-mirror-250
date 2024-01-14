# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from ..rootresource import RootResource
from .domain import Domain
from .organization import Organization
from .project import Project
from .namespace import Namespace as NamespaceType


class Namespace(RootResource[Organization | Project | Domain | NamespaceType]):
    """A `Namespace` provides a mechanism for isolating groups of resources.
    Names of resources need to be unique within a namespace, but not across
    namespaces. Namespace-based scoping is applicable only for namespaced
    objects and not for system-wide objects
    """
    model_config = {'populate_by_name': True}

    @classmethod
    def factory(cls, type: str, name: str, **extra: Any):
        params: dict[str, Any] = {
            'metadata': {
                'name': name
            },
            'type': type
        }
        return cls.model_validate({**extra, **params})

    @classmethod
    def is_namespaced(cls) -> bool:
        return False