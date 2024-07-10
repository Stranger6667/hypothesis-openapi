# ruff: noqa: F722, F821
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, TypeAlias

from ._common import (
    RESPONSE_SUCCESS,
    Info,
    reference,
    PATH_ITEM_SAMPLE,
    PathItemReference,
    Response,
)
from ._types import Missing, Pattern, UniqueList

PARAMETER_SAMPLE = {"name": "sample", "in": "query", "schema": {"type": "string"}}
ResponseId: TypeAlias = Pattern[r"^[1-5](?:[0-9]{2}|XX)$|^(default)\Z"]  # type: ignore[type-arg,valid-type]
ParameterReference = reference("#/components/parameters/SampleParameter")
ResponseReference = reference("#/components/responses/Success")


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

    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["in"] = value.pop("in_")
        value["schema"] = {"type": "string"}
        if value["in"] == "path":
            value["required"] = True
        return value

    def __hash__(self) -> int:
        return hash((self.name, self.in_))


ParameterList: TypeAlias = UniqueList[Parameter | ParameterReference]  # type: ignore[type-arg,valid-type]
