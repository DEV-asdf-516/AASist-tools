from enum import Enum
from typing import Dict, List

from aasist.src.module.tester.extends.context.extends_validation_context import (
    ExtendsValidationContext,
)
from aas_test_engines.reflect import TypeBase
from aas_test_engines.test_cases.v3_0.model import Referable, HasSemantics, DataElement


class _AasdContextRules(Enum):
    parse_concrete_object = "parse_concrete_object"


class AasdValidationContext(ExtendsValidationContext):
    _DATA_CLASS = {
        "Referable": Referable,
        "HasSemantics": HasSemantics,
        "DataElement": DataElement,
        "AnnotatedRelationshipElement": DataElement,
    }

    def __init__(self):
        super().__init__()

    def __enter__(self):
        self.constraints_store: Dict[str, List[TypeBase]] = {}
        self.parents_store: Dict[str, List[TypeBase]] = {
            "Referable": [],
            "HasSemantics": [],
            "DataElement": [],
            "AnnotatedRelationshipElement": [],
        }
        self._petch_parse()
        return self

    def _petch_parse(self):
        from aas_test_engines.test_cases.v3_0 import parse as parse_module
        from aas_test_engines.reflect import ClassType
        from aas_test_engines.test_cases.v3_0.adapter import (
            Adapter,
            AdapterException,
        )
        from aas_test_engines.result import AasTestResult

        original_parse_concrete_object = parse_module.parse_concrete_object
        self.original_methods[_AasdContextRules.parse_concrete_object.value] = (
            parse_module,
            "parse_concrete_object",
            original_parse_concrete_object,
        )

        def aasd_parse_concrete_object(
            cls: ClassType, adapter: Adapter, result: AasTestResult
        ):
            try:
                obj = adapter.as_object()
            except AdapterException:
                return parse_module.INVALID

            args = {}
            all_fields = set()
            for field in cls.attrs:
                field_name = field.force_name or parse_module.to_lower_camel_case(
                    field.name
                )
                all_fields.add(field_name)
                try:
                    obj_value = obj[field_name]
                except KeyError:
                    if field.required:
                        args[field.name] = parse_module.INVALID
                    else:
                        args[field.name] = None
                    continue
                args[field.name] = parse_module.parse(field.type, obj_value, result)

            construct = cls.construct(args)
            check_constraints = [
                attr
                for i in dir(construct)
                if "aasd" in i and (attr := getattr(construct, i)) is not None
            ]

            if check_constraints:
                self.constraints_store.setdefault(construct.__class__.__name__, [])

                for data_class in self.parents_store.keys():
                    if issubclass(construct.__class__, self._DATA_CLASS[data_class]):
                        self.parents_store[data_class].append(construct)

                self.constraints_store[construct.__class__.__name__].append(construct)

            return cls.construct(args)

        parse_module.parse_concrete_object = aasd_parse_concrete_object
