"""Helper classes for the editor"""
from typing import Union, TypeVar
import os
T = TypeVar("T")

class Counter:
    """Class to create a counter with a defined range. The counter can
    be incremented or decremented within the range and the value
    will be clamped to the range if it goes outside of it. If the
    strict flag is set, a ValueError will be raised if the value
    goes outside of the range."""
    def __init__(self, value: int, min_val: int, max_val: int, *, strict: bool = False):
        self._min = min_val
        self._max = max_val
        self.strict = strict

        # Validate initial value
        if not min_val <= value <= max_val:
            if strict:
                raise ValueError(f"Initial value {value} must be between {min_val} and {max_val}")
            else:
                # Fix the value by clamping it
                value = min(max(value, min_val), max_val)

        self.value = value

    def __int__(self):
        return self.value

    def __add__(self, other: int) -> 'Counter':
        result_value = int(self) + other

        if not self._min <= result_value <= self._max:
            if self.strict:
                raise ValueError(f"Result {result_value} must be between {self._min} and {self._max}")
            else:
                # Fix the value by clamping it
                result_value = min(max(result_value, self._min), self._max)

        return Counter(result_value, self._min, self._max, strict=self.strict)

    def __sub__(self, other: int) -> 'Counter':
        result_value = int(self) - other

        if not self._min <= result_value <= self._max:
            if self.strict:
                raise ValueError(f"Result {result_value} must be between {self._min} and {self._max}")
            else:
                # Fix the value by clamping it
                result_value = min(max(result_value, self._min), self._max)

        return Counter(result_value, self._min, self._max, strict=self.strict)

    def __repr__(self) -> str:
        mode = "strict" if self.strict else "non-strict"
        return f"Counter(value={int(self)}, bounds=[{self._min}, {self._max}], mode='{mode}')"

    def __eq__(self, other: Union[int,'Counter']):
        return int(other) == int(self)

class AttrDict(dict):
    """
    A dict subclass that allows attribute access like an object.

    Instead of dict[key], you can use dict.key.

    This is useful when you want to use a dict as a simple dataclass, but
    you can still use it as a dict if you need to.

    Example:

        attr_dict = AttrDict()
        attr_dict.foo = 'bar'
        print(attr_dict.foo)  # prints 'bar'
        print(attr_dict['foo'])  # prints 'bar'
    """
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"type object '{type(self).__name__}' has no attribute '{attr}'") from None

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        try:
            del self[attr]
        except KeyError:
            raise AttributeError(f"type object '{type(self).__name__}' has no attribute '{attr}'") from None

    def __dir__(self):
        return list(self) + dir(type(self))

    def __repr__(self):
        return f"AttrDict({dict.__repr__(self)})"


def subtract_vectors(*vectors: tuple[int, int]) -> tuple[int, int]:
    """ Subtract 2D vectors"""
    result = vectors[0]
    for vector in vectors[1:]:
        result = (result[0] - vector[0], result[1] - vector[1])
    return result


def add_vectors(*vectors: tuple[int, int]) -> tuple[int, int]:
    """Subtract 2D vectors until a single vector is left."""
    result = vectors[0]
    for vector in vectors[1:]:
        result = (result[0] + vector[0], result[1] + vector[1])
    return result


def instantiate(*args, **kwargs):
    """
    A decorator that instantiates the class with the given arguments.
    
    Args:
        *args: arguments to pass to the class constructor
        *kwargs: keyword arguments to pass to the class constructor
    
    Returns:
        An instance of the class.

    Example:
    >>> @instantiate()
    ... class A:
    ...     pass
    ...
    >>> @instantiate(5)
    ... class B:
    ...     def __init__(self, value):
    ...         self.value = value
    ...
    >>> print(B.value)
    5
    """
    def decorator(cls: type[T]) -> T:
        return cls(*args, **kwargs)
    return decorator


def quick_load(name: str, dpath: str):
    """ load a file and return the data as a string """
    if not os.path.exists(dpath):
        print(f"WARNING: no json file found for {name!r} ({dpath!r})")
        return None
    with open(dpath, encoding="UTF-8") as f:
        data = f.read()
    return data
