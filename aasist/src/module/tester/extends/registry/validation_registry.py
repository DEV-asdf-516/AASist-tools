import asyncio
from enum import Enum
from typing import Iterable, List, Union
from aasist.src.gui.handler import _TEST_LOG_NAME, LogLevel, QueueHandler
from aasist.src.module.tester.extends.registry.validation import Validation
from aas_test_engines.reflect import TypeBase
from aas_test_engines.test_cases.v3_0.parse import CheckConstraintException


class ValidationRegistry:
    _registry = Validation()
    results: dict[str, bool] = {}
    log_handler = QueueHandler(_TEST_LOG_NAME)

    @classmethod
    def get_validator(cls, name: str):
        return cls._registry.get_validator(name)

    @classmethod
    def validator(cls, *validators: Iterable[str]):
        return cls._registry.register(*validators)

    async def check_rule_with_logging(
        self, objects: List[TypeBase], method_name: Union[str, List[str]], rule: Enum
    ):
        self.results[rule] = self.results.get(rule, True)
        for obj in objects:
            if hasattr(obj, method_name) is False:
                continue
            try:
                message = getattr(obj, method_name)()
                if not message:
                    continue
                await asyncio.sleep(0.1)
                self.log_handler.add(
                    message,
                    log_level=LogLevel.ERROR,
                )
                self.results[rule] = False
            except CheckConstraintException as e:
                await asyncio.sleep(0.1)
                id = getattr(obj, "id_short", None)
                keys = getattr(obj, "keys", None)
                if not id and keys:
                    values = [
                        key.value.raw_value
                        for key in keys
                        if getattr(key, "value", None)
                        and getattr(key.value, "raw_value", None) is not None
                    ]
                    if values:
                        id = ", ".join(values)
                self.log_handler.add(
                    (
                        f'- {obj.__class__.__name__} "{id}"" is {e}'
                        if id
                        else f"- {obj.__class__.__name__} is {e}"
                    ),
                    log_level=LogLevel.ERROR,
                )
                self.results[rule] = False
            except TypeError as e:
                pass
