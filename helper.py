from typing import Union

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

