# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import overload
from typing import Any
from typing import Literal
from typing import Protocol
from typing import TypeVar

from .itransaction import ITransaction
from .ityped import ITyped

T = TypeVar('T')


class IStorage(Protocol):
    """The interface for storage classes. A storage class knows how
    to retrieve and persist objects of a specific type.
    """

    @overload
    async def get(self, key: ITyped[T], model: type[T] | None, cached: Literal[True], **kwargs: Any) -> tuple[T, bool]:
        ...

    @overload
    async def get(self, key: ITyped[T], model: type[T] | None, cached: Literal[False], **kwargs: Any) -> T:
        ...

    async def get(
        self,
        key: ITyped[T],
        model: type[T] | None = None,
        cached: bool = False,
        max_age: int = 0,
        transaction: ITransaction | None = None,
        **kwargs: Any
    ) -> T | tuple[T, bool]:
        ...

    async def delete(
        self,
        object: T,
        transaction: ITransaction | None = None,
        **kwargs: Any
    ) -> T: ...

    async def first(
        self,
        model: type[T],
        sort: list[str] | None = None,
        transaction: ITransaction | None = None,
        **kwargs: Any
    ) -> T | None:
        ...

    async def persist(
        self,
        object: T,
        transaction: ITransaction | None = None,
        **kwargs: Any
    ) -> T:
        ...

    async def pop(
        self,
        key: ITyped[T] | int | str,
        model: type[T] | None = None,
        sort: list[str] | None = None,
        transaction: ITransaction | None = None,
        **kwargs: Any
    ) -> T:
        ...