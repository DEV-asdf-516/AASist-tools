from functools import wraps
from typing import Callable, Dict, Iterable


class Validation:

    def __init__(self):
        self._validators: Dict[str, Callable] = {}

    def register(self, *validators: Iterable[str]):
        def decorator(func):
            for name in validators:

                @wraps(func)
                async def wrapper(*args, rule=name, **kwargs):
                    return await func(*args, rule=rule, **kwargs)

                self._validators[name] = wrapper
            return func

        return decorator

    def get_validator(self, validator: str) -> Callable:
        return self._validators.get(validator)
