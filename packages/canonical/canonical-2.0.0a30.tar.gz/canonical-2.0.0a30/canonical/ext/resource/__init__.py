# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .error import Error
from .iresourcequery import IResourceQuery
from .iresourcerepository import IResourceRepository
from .namespace import Namespace
from .namespacedobjectmeta import NamespacedObjectMeta
from .namespacedobjectreference import NamespacedObjectReference
from .objectmeta import ObjectMeta
from .objectreference import ObjectReference
from .resource import M as ObjectMetaType
from .resource import Resource
from .rootresource import ResourceType
from .rootresource import ResourceTypeVar
from .rootresource import RootResource
from .transientmeta import TransientMeta


__all__: list[str] = [
    'Error',
    'IResourceQuery',
    'IResourceRepository',
    'Namespace',
    'NamespacedObjectMeta',
    'NamespacedObjectReference',
    'ObjectMeta',
    'ObjectMetaType',
    'ObjectReference',
    'Resource',
    'ResourceType',
    'ResourceTypeVar',
    'RootResource',
    'TransientMeta',
]