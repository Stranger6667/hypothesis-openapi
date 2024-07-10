# ruff: noqa: F722, F821
from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class Info:
    version: Literal["1.0.0"]
    title: Literal["Example API"]


@dataclass
class PathItemReference:
    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["$ref"] = "#/x-paths/Entry"
        return value


@dataclass
class ParameterReference:
    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["$ref"] = "#/parameters/SampleParameter"
        return value

    def __hash__(self) -> int:
        return hash(("$ref", "#/parameters/SampleParameter"))


@dataclass
class Response:
    description: Literal["Ok"]


@dataclass
class ResponseReference:
    def map_value(self, value: dict[str, Any]) -> dict[str, Any]:
        value["$ref"] = "#/responses/Success"
        return value


RESPONSE_SUCCESS = {"description": "OK"}
PATH_ITEM_SAMPLE = {"get": {"responses": {"default": RESPONSE_SUCCESS}}}
