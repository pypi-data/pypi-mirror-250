# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import datetime
import uuid
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import TYPE_CHECKING

import pydantic

from canonical.utils import deephash
if TYPE_CHECKING:
    from .resource import Resource
from .resourcekey import ResourceKey


N = TypeVar('N')
ObjectMetaType = N


class ObjectMeta(pydantic.BaseModel, Generic[N]):
    model_config = {'populate_by_name': True}
    _version: str = pydantic.PrivateAttr()
    _kind: str = pydantic.PrivateAttr()

    annotations: dict[str, Any] = pydantic.Field(
        default_factory=dict,
        title="Annotations",
        description=(
            "Annotations is an unstructured key value map stored with "
            "a resource that may be set by external tools to store "
            "and retrieve arbitrary metadata. They are not queryable and "
            "should be preserved when modifying objects."
        )
    )
    
    created: datetime.datetime | None = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        title="Created",
        description=(
            "`created` is a timestamp representing the server time "
            "when this object was created. It is not guaranteed to be set in "
            "happens-before order across separate operations. Clients may not "
            "set this value. It is represented in RFC3339 form and is in UTC. "
            "Populated by the system. Read-only. Null for lists."
        ),
        frozen=True
    )
    
    deleted: datetime.datetime | None = pydantic.Field(
        default=None,
        title="Deleted",
        description=(
            "The `deleted` field is an RFC 3339 date and time "
            "at which this resource will be deleted. This field "
            "is set by the server when a graceful deletion is "
            "requested by the user, and is not directly settable "
            "by a client. The resource is expected to be deleted "
            "(no longer visible from resource lists, and not "
            "reachable by name) after the time in this field. "
            "Once set, this value may not be unset or be set "
            "further into the future, although it may be shortened "
            "or the resource may be deleted prior to this time."
        ),
    )

    finalizers: set[str] = pydantic.Field(
        default_factory=set,
        description=(
            "Must be empty before the object is deleted from the registry. "
            "Each entry is an identifier for the responsible component that "
            "will remove the entry from the list. If the `deleted` field "
            "of the object is non-nil, entries in this list can only be "
            "removed. Finalizers may be processed and removed in any order."
        )
    )

    updated: datetime.datetime | None = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        title="Updated",
        description=(
            "`CreationTimestamp` is a timestamp representing the server time "
            "when this object was updated. Clients may not "
            "set this value. It is represented in RFC3339 form and is in UTC. "
            "Populated by the system. Read-only. Null for lists."
        )
    )

    generation: int = pydantic.Field(
        default=1,
        title="Generation",
        description=(
            "A sequence number representing a specific generation "
            "of the state. Populated by the system. Read-only."
        )
    )

    labels: dict[str, str | None] = pydantic.Field(
        default_factory=dict,
        title="Labels",
        description=(
            "Map of string keys and values that can be used to organize and "
            "categorize (scope and select) objects."
        )
    )

    name: N = pydantic.Field(
        default=...,
        title="Name",
        description=(
            "Name must be unique within a namespace. Is required when creating "
            "resources, although some resources may allow a client to request "
            "the generation of an appropriate name automatically. Name is "
            "primarily intended for creation idempotence and configuration "
            "definition. Cannot be updated."
        ),
        frozen=True
    )

    generate_name: str | None = pydantic.Field(
        default=None,
        alias='generateName',
        description=(
            "An optional prefix, used by the server, to generate a unique name "
            "ONLY IF the `name` field has not been provided. If this field "
            "is used, the name returned to the client will be different than "
            "the name passed. This value will also be combined with a unique "
            "suffix. The provided value has the same validation rules as the "
            "`name` field, and may be truncated by the length of the suffix "
            "required to make the value unique on the server. If this field "
            "is specified and the generated name exists, the server will "
            "return a 409. Applied only if `name` is not specified."
        ),
        exclude=True
    )

    resource_version: str = pydantic.Field(
        default='',
        alias='resourceVersion',
        description=(
            "An opaque value that represents the internal version of this object "
            "that can be used by clients to determine when objects have changed. "
            "May be used for optimistic concurrency, change detection, and the "
            "watch operation on a resource or set of resources. Clients must "
            "treat these values as opaque and passed unmodified back to the "
            "server. They may only be valid for a particular resource or set "
            "of resources. Populated by the system. Read-only. Value must be "
            "treated as opaque by clients and ."
        )
    )

    tags: set[str] = pydantic.Field(
        default_factory=set,
        description=(
            "An array of tags that may be used to classify an object "
            "if a label or annotation is not applicable."
        )
    )

    uid: str = pydantic.Field(
        default_factory=lambda: str(uuid.uuid4()),
        title="UID",
        description=(
            "UID is the unique in time and space value for this object. "
            "It is typically generated by the server on successful creation "
            "of a resource and is not allowed to change on PUT operations. "
            "Populated by the system. Read-only."
        ),
        frozen=True
    )

    @property
    def key(self) -> ResourceKey[N]:
        return ResourceKey(api_version=self._api_version, kind=self._kind, name=self.name)

    @classmethod
    def is_namespaced(cls) -> bool:
        return False

    @classmethod
    def default(cls) -> 'ObjectMeta[Any]':
        raise ValueError("Can not create ObjectMeta without parameters.")

    def attach(self, resource: Resource[Any]):
        self._api_version = resource.api_version
        self._kind = resource.kind

    def get_namespace(self) -> str | None:
        return None

    def is_labeled(self, names: list[str]) -> bool:
        return all([
            self.labels.get(name) not in {None, 'null'}
            for name in names
        ])

    def update_resource_version(self, data: dict[str, Any]):
        state = self.model_dump(mode='json', include={
            'annotations',
            'labels',
            'name',
            'tags'
        })
        self.resource_version = deephash([
            deephash(state),
            deephash(data)
        ], encode='hex')