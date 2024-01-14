# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import get_args
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Literal
from typing import TypeAlias
from typing import TypeVar

import pydantic

from canonical.protocols import IStorage
from canonical import ResourceName
from canonical import TypedResourceName
from .listbase import ListBase
from .resource import Resource

__all__: list[str] = [
    'RootResource'
]

T = TypeVar('T', bound=Resource[Any])
S = TypeVar('S', bound='RootResource[Any]')


class RootResource(pydantic.RootModel[T], Generic[T]):
    _is_namespaced: bool
    group: ClassVar[str]
    base_path: ClassVar[str]
    plural: ClassVar[str]
    List: ClassVar[type[ListBase[Any, Any]]]
    ResourceName: ClassVar[type[TypedResourceName[Any]]]

    @property
    def api_version(self):
        return self.root.api_version

    @property
    def key(self):
        return self.root.key

    @property
    def kind(self):
        return self.root.kind

    @property
    def metadata(self):
        return self.root.metadata

    @property
    def relname(self):
        return self.root.relname

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any):
        paths: set[str] = set()
        types = get_args(cls.model_fields['root'].annotation)
        for model in types:
            paths.add(model.base_path)
        if len(paths) > 1:
            raise ValueError(f"All root models must have the same base path.")
        if paths:
            cls.base_path = types[0].base_path
            cls.group = types[0].group
            cls.plural = types[0].plural
            cls._namespaced = types[0].is_namespaced()
        cls.ResourceName = ResourceName.subclass(cls) # type: ignore
        cls.List = type(f'{cls.__name__}List', (ListBase[Literal[f'{cls.__name__}List'], cls],), {
            'items': pydantic.Field(
                default_factory=list,
                description=(
                    "The `items` member contains an array "
                    f"of `{cls.__name__}` objects."
                )
            ),
            '__annotations__': {'items': list[cls]}
        })
        cls.List.model_fields['kind'].default = f'{cls.__name__}List'
        cls.List.model_rebuild()

        cls.model_config.update({
            'title': cls.__name__
        })
        cls.model_rebuild()

    @classmethod
    def is_destroyable(cls) -> bool:
        return True

    @classmethod
    def is_namespaced(cls) -> bool:
        return cls._is_namespaced

    @classmethod
    def is_purgable(cls) -> bool:
        return True

    def get_namespace(self) -> str | None:
        return self.root.get_namespace()

    def get_resource_name(self: S, service: str) -> TypedResourceName[S]:
        return self.ResourceName(self.root.get_resource_name(service))

    def model_dump_yaml(self, **kwargs: Any):
        return self.root.model_dump_yaml(**kwargs)

    async def persist(self, storage: IStorage | None):
        return self.root.persist(storage)


ResourceType: TypeAlias = Resource[Any] | RootResource[Any]
ResourceTypeVar = TypeVar('ResourceTypeVar', bound=ResourceType)