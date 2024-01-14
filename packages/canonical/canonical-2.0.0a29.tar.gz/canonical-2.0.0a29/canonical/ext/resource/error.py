# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import uuid
from typing import Any

import pydantic

from canonical.utils.http import Request
from .resource import Resource
from .objectmeta import ObjectMeta


class ErrorData(pydantic.BaseModel):
    model_config = {'populate_by_name': True}

    detail: str = pydantic.Field(
        default=...,
        description="A summary of the error."
    )


class HTTPErrorData(ErrorData):
    status_code: int = pydantic.Field(
        default=...,
        alias='statusCode',
        description=(
            "The HTTP status code identifying the error state."
        )
    )

    request: Request = pydantic.Field(
        default=...,
        description=(
            "Describes the HTTP request that caused the error "
            "condition."
        )
    )


class Error(Resource[ObjectMeta[str]], version='errors/v1'):
    data: HTTPErrorData

    @classmethod
    def factory(cls, data: dict[str, Any]):
        return cls.model_validate({
            'metadata': {
                'name': str(uuid.uuid4())
            },
            'data': data
        })