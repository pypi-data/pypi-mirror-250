# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Literal
from typing import TypeVar

import pydantic

from ..resource import Resource
from ..resource import M


S = TypeVar('S')


class BaseNamespace(Resource[M], Generic[M], kind='Namespace', version='namespaces/v1'):
    __abstract__: ClassVar[bool] = True
    model_config = {'populate_by_name': True}

    type: str = pydantic.Field(
        default=...,
        description=(
            "Used to discriminate between various namespace types."
        )
    )

    def __init_subclass__(cls, type: str | None = None, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        if type is None and not cls.__abstract__:
            raise ValueError(
                f"The `type` class parameter must be specified on {cls.__name__}."
            )
        cls.__abstract__ = False
        cls.model_fields['type'].annotation = Literal[type] # type: ignore
        cls.model_fields['type'].default = type
        cls.model_rebuild()