from typing import Annotated

from hypothesis import strategies as st


class Pattern:
    def __class_getitem__(cls, pattern: str) -> object:
        strategy = st.from_regex(pattern)
        return Annotated[str, strategy]


class UniqueList:
    def __class_getitem__(cls, inner: type) -> object:
        strategy = st.lists(st.from_type(inner), unique=True)
        return Annotated[list, strategy]


class CombinedDict:
    def __class_getitem__(cls, args: tuple[type, type, dict]) -> object:
        keys, values, defaults = args

        def update(data: dict) -> dict:
            data.update(defaults)
            return data

        strategy = st.dictionaries(st.from_type(keys), st.from_type(values)).map(update)
        return Annotated[dict, strategy]


class Missing:
    pass
