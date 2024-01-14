# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

from canonical.ext.resource import NamespacedObjectMeta
from .baserolebinding import BaseRoleBinding


class RoleBinding(
    BaseRoleBinding[NamespacedObjectMeta[str]],
    kind=Literal['ClusterRole', 'Role'],
    version='rolebindings.iam.webiam.io/v1'
):
    pass