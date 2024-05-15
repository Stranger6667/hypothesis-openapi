from typing import Any, Literal
from hypothesis import strategies as st
from ._v2 import Swagger
from ._serialize import asdict


def openapis(version: Literal["2.0"] | Literal["3.0"] | Literal["3.1"]) -> "st.SearchStrategy[dict[str, Any]]":
    if version == "2.0":
        return st.from_type(Swagger).map(asdict)  # type: ignore[arg-type]
    raise ValueError(f"Unsupported version: {version}")
