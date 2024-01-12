import re
from typing import (
    Any,
    Optional,
    Union,
)


def catch_str(
    value: str,
    key: str,
    *,
    replace: Optional[str] = None,
    flag: bool = True,
) -> tuple[str, Optional[Union[bool, str]]]:
    """Catch keyword from string value and return True if exits"""
    if key in value:
        return (
            " ".join(value.replace(key, (replace or "")).split()),
            (True if flag else key),
        )
    return value, (False if flag else None)


def split_dtype(dtype: str) -> tuple[str, str]:
    """Split the datatype value from long string by null string"""
    _nullable: str = "null"
    for null_str in ["not null", "null"]:
        if re.search(null_str, dtype):
            _nullable = null_str
            dtype = dtype.replace(null_str, "")
    return " ".join(dtype.strip().split()), _nullable


def only_one(
    check_list: list[Any],
    match_list: list[Any],
    default: bool = True,
) -> Any:
    """Get only one value from the checking list that match with ordered value on
    the matching list.
        Examples:
        >>> list_a = ['a', 'a', 'b']
        >>> list_b = ['a', 'b', 'c']
        >>> list_c = ['d', 'f']
        >>> only_one(list_a, list_b)
        'a'
        >>> only_one(list_c, list_b)
        'a'
    """
    if len(exist := set(check_list).intersection(set(match_list))) == 1:
        return list(exist)[0]
    return next(
        (_ for _ in match_list if _ in check_list),
        (match_list[0] if default else None),
    )
