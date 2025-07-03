from enum import Enum
from aasist.src.module.tester.extends.context.extends_validation_context import (
    ExtendsValidationContext,
)


class _LenientContextRules(Enum):
    parse_concrete_object = "parse_concrete_object"


# 제약조건 무시
class LenientValidationContext(ExtendsValidationContext):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        pass
        # TODO
