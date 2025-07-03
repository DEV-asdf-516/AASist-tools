from typing import Iterable
from aasist.src.module.tester.extends.registry.validation import Validation


class ValidationRegistry:
    _registry = Validation()

    @classmethod
    def get_validator(cls, name: str):
        return cls._registry.get_validator(name)

    @classmethod
    def validator(cls, *validators: Iterable[str]):
        return cls._registry.register(*validators)
