from dataclasses import is_dataclass, fields
from hypothesis import strategies as st
from ._types import Missing


@st.composite  # type: ignore[misc]
def asdict(draw: st.DrawFn, _obj: object) -> object:
    def _asdict(obj: object) -> object:
        if is_dataclass(obj):
            result = {}
            for f in fields(obj):
                value = getattr(obj, f.name)
                if not isinstance(value, Missing):
                    result[f.name] = _asdict(value)
            if hasattr(obj, "map_value"):
                result = obj.map_value(result)
            return result
        elif isinstance(obj, (list, tuple)):
            return type(obj)(_asdict(v) for v in obj)
        elif isinstance(obj, dict):
            return type(obj)((_asdict(k), _asdict(v)) for k, v in obj.items())
        return obj

    return _asdict(_obj)
