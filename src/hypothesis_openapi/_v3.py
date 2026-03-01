# ruff: noqa: F722, F821
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypeAlias

from ._common import (
    DEFAULT_SECURITY_SCHEME,
    PATH_ITEM_SAMPLE,
    RESPONSE_SUCCESS,
    Info,
    OperationSecurityRequirement,
    PathItemReference,
    Response,
    reference,
)
from ._types import CombinedDict, Missing, Pattern, UniqueList

PARAMETER_SAMPLE = {"name": "sample", "in": "query", "schema": {"type": "string"}}
ResponseId: TypeAlias = Pattern[r"^[1-5](?:[0-9]{2}|XX)$|^(default)\Z"]  # type: ignore[type-arg,valid-type]
ParameterReference = reference("#/components/parameters/SampleParameter")
ResponseReference = reference("#/components/responses/Success")

RequestBodyMediaType = (
    Literal["application/json"] | Literal["application/x-www-form-urlencoded"] | Literal["multipart/form-data"]
)

_REQUEST_BODY_DEFAULTS: dict[str, dict] = {"application/json": {"schema": {}}}

_VALID_STYLES: dict[str, frozenset] = {
    "query": frozenset({"form", "spaceDelimited", "pipeDelimited", "deepObject"}),
    "path": frozenset({"simple", "label", "matrix"}),
    "header": frozenset({"simple"}),
    "cookie": frozenset({"form"}),
}


@dataclass
class MediaTypeObject:
    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["schema"] = {}
        return value


@dataclass
class RequestBody:
    required: bool | Missing
    content: CombinedDict[RequestBodyMediaType, MediaTypeObject, _REQUEST_BODY_DEFAULTS]  # type: ignore[type-arg,valid-type]


@dataclass
class StringSchema:
    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        return {"type": "string"}


@dataclass
class ArraySchema:
    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        return {"type": "array", "items": {"type": "string"}}


@dataclass
class ObjectSchema:
    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        return {"type": "object", "additionalProperties": {"type": "string"}}


ParameterSchema = StringSchema | ArraySchema | ObjectSchema


@dataclass
class OpenApi30:
    openapi: Pattern[r"^3\.0\.[0-9]\Z"]  # type: ignore[type-arg,valid-type]
    info: Info
    paths: dict[Pattern["^/"], PathItem | PathItemReference]  # type: ignore[type-arg,valid-type]

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["x-paths"] = {"Entry": PATH_ITEM_SAMPLE}
        value["components"] = {
            "parameters": {"SampleParameter": PARAMETER_SAMPLE},
            "responses": {"Success": RESPONSE_SUCCESS},
            "securitySchemes": {DEFAULT_SECURITY_SCHEME: {"type": "apiKey", "name": "X-Api-Key", "in": "header"}},
        }
        return value


@dataclass
class PathItem:
    get: Operation | Missing
    put: Operation | Missing
    post: Operation | Missing
    delete: Operation | Missing
    options: Operation | Missing
    head: Operation | Missing
    patch: Operation | Missing
    trace: Operation | Missing
    parameters: ParameterList | Missing


@dataclass
class Operation:
    operationId: str | Missing
    parameters: ParameterList | Missing
    tags: UniqueList[str] | Missing  # type: ignore[type-arg,valid-type]
    responses: dict[ResponseId, Response | ResponseReference]  # type: ignore[valid-type]
    requestBody: RequestBody | Missing
    security: OperationSecurityRequirement | Missing
    deprecated: bool | Missing

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        if not value["responses"]:
            value["responses"] = {"default": RESPONSE_SUCCESS}
        return value


@dataclass
class Parameter:
    name: str
    in_: Literal["query", "header", "path", "cookie"]
    required: bool
    deprecated: bool
    allowEmptyValue: bool
    allowReserved: bool
    explode: bool
    style: Literal["form", "simple", "label", "matrix", "spaceDelimited", "pipeDelimited", "deepObject"] | Missing
    schema: ParameterSchema

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        in_ = value.pop("in_")
        value["in"] = in_
        if in_ == "path":
            value["required"] = True
        style = value.get("style")
        if style is not None and style not in _VALID_STYLES.get(in_, frozenset()):
            del value["style"]
        return value

    def __hash__(self) -> int:
        return hash((self.name, self.in_))


ParameterList: TypeAlias = UniqueList[Parameter | ParameterReference]  # type: ignore[type-arg,valid-type]
