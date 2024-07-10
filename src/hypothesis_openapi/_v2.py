# ruff: noqa: F722, F821
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TypeAlias

from ._common import (
    PATH_ITEM_SAMPLE,
    RESPONSE_SUCCESS,
    Info,
    reference,
    PathItemReference,
    Response,
)
from ._types import CombinedDict, Missing, Pattern, UniqueList

PARAMETER_SAMPLE = {"name": "sample", "in": "query", "type": "string"}
ResponseId: TypeAlias = Pattern[r"^([0-9]{3})$|^(default)\Z"]  # type: ignore[type-arg,valid-type]
ParameterReference = reference("#/parameters/SampleParameter")
ResponseReference = reference("#/responses/Success")

MediaType = (
    Literal["application/json"]
    | Literal["application/xml"]
    | Literal["text/plain"]
    | Literal["text/yaml"]
    | Literal["application/x-www-form-urlencoded"]
    | Literal["multipart/form-data"]
    | Literal["application/octet-stream"]
)


@dataclass
class Swagger:
    swagger: Literal["2.0"]
    info: Info
    host: Pattern["^[^{}/ :\\\\]+(?::\\d+)?$"] | Missing  # type: ignore[type-arg,valid-type]
    basePath: Pattern["^/"] | Missing  # type: ignore[type-arg,valid-type]
    paths: dict[Pattern["^/"], PathItem | PathItemReference]  # type: ignore[type-arg,valid-type]
    consumes: MediaTypeList | Missing
    produces: MediaTypeList | Missing
    parameters: CombinedDict[str, Parameter, {"SampleParameter": PARAMETER_SAMPLE}]  # type: ignore[type-arg,valid-type]
    responses: CombinedDict[ResponseId, Response, {"Success": RESPONSE_SUCCESS}]  # type: ignore[type-arg,valid-type]
    definitions: Definitions

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["x-paths"] = {"Entry": PATH_ITEM_SAMPLE}
        return value


@dataclass
class Definitions:
    pass


@dataclass
class PathItem:
    get: Operation | Missing
    put: Operation | Missing
    post: Operation | Missing
    delete: Operation | Missing
    options: Operation | Missing
    head: Operation | Missing
    patch: Operation | Missing
    parameters: ParameterList | Missing


@dataclass
class Operation:
    operationId: str | Missing
    parameters: ParameterList | Missing
    tags: UniqueList[str] | Missing  # type: ignore[type-arg,valid-type]
    consumes: MediaTypeList | Missing
    produces: MediaTypeList | Missing
    responses: dict[ResponseId, Response | ResponseReference]  # type: ignore[valid-type]

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        if not value["responses"]:
            value["responses"] = {"default": RESPONSE_SUCCESS}
        return value


@dataclass
class BodyParameter:
    name: str
    schema: dict = field(default_factory=dict)

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["in"] = "body"
        return value

    def __hash__(self) -> int:
        return hash((self.name, "body"))


@dataclass
class QueryParameter:
    name: str
    type: Literal["string", "number", "boolean", "integer", "array"]

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["in"] = "query"
        return value

    def __hash__(self) -> int:
        return hash((self.name, "query"))


@dataclass
class HeaderParameter:
    name: str
    type: Literal["string", "number", "boolean", "integer", "array"]

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["in"] = "header"
        return value

    def __hash__(self) -> int:
        return hash((self.name, "header"))


@dataclass
class PathParameter:
    name: str
    type: Literal["string", "number", "boolean", "integer", "array"]

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["in"] = "path"
        value["required"] = True
        return value

    def __hash__(self) -> int:
        return hash((self.name, "path"))


@dataclass
class FormDataParameter:
    name: str
    type: Literal["string", "number", "boolean", "integer", "array", "file"]

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["in"] = "formData"
        return value

    def __hash__(self) -> int:
        return hash((self.name, "formData"))


Parameter = BodyParameter | QueryParameter | HeaderParameter | PathParameter | FormDataParameter
ParameterList: TypeAlias = UniqueList[Parameter | ParameterReference]  # type: ignore[type-arg, valid-type]
MediaTypeList: TypeAlias = UniqueList[MediaType]  # type: ignore[type-arg]
