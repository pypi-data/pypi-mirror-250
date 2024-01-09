"""Type for Forager project."""
from typing import Callable, TypeAlias, TypedDict

Dict_A: TypeAlias = dict[str, str | int]
Callable_A: TypeAlias = Callable[[str, Dict_A], None]
Callable_B: TypeAlias = Callable[[str, str], None]
Callable_C: TypeAlias = Callable[[str, int], None]
Tuple_A: TypeAlias = tuple[Callable_A, ...]
Tuple_B: TypeAlias = tuple[Callable_B, ...]
Tuple_C: TypeAlias = tuple[Callable_C, ...]


class ValidatorTypeDict(TypedDict, total=False):
    """Type for validators dict."""

    domain: Tuple_B
    company: Tuple_B
    limit: Tuple_C
    offset: Tuple_C
    type: Tuple_B
    seniority: Tuple_B
    department: Tuple_B
    required_field: Tuple_B
    first_name: Tuple_B
    last_name: Tuple_B
    full_name: Tuple_B
    max_duration: Tuple_C
    email: Tuple_B
    required_arguments: Tuple_A
