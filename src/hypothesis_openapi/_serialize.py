from dataclasses import is_dataclass, fields

from ._types import Missing


def asdict(obj: object) -> object:
    if is_dataclass(obj):
        result = {}
        for f in fields(obj):
            value = getattr(obj, f.name)
            if not isinstance(value, Missing):
                result[f.name] = asdict(value)
        if hasattr(obj, "map_value"):
            result = obj.map_value(result)
        return result
    elif isinstance(obj, (list, tuple)):
        return type(obj)(asdict(v) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((asdict(k), asdict(v)) for k, v in obj.items())
    return obj
