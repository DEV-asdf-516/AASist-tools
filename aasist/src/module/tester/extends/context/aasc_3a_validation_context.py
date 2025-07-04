from enum import Enum
from typing import Dict, List

from aasist.src.module.tester.extends.context.extends_validation_context import (
    ExtendsValidationContext,
)
from aas_test_engines.reflect import TypeBase
from aas_test_engines.test_cases.v3_0.model import (
    Referable,
    DataSpecificationIec61360,
)


class _Aasc3aContextRules(Enum):
    parse_concrete_object = "parse_concrete_object"


class Aasc3aValidationContext(ExtendsValidationContext):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        self.constraints_store: Dict[str, List[TypeBase]] = {
            "DataSpecificationIec61360": [],
            "ConceptDescription": [],
            "Submodel": [],
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
        self.original_methods[_Aasc3aContextRules.parse_concrete_object.value] = (
            parse_module,
            "parse_concrete_object",
            original_parse_concrete_object,
        )

        def aasc_3a_parse_concrete_object(
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

            if issubclass(construct.__class__, Referable) and getattr(
                construct.id_short, "raw_value", None
            ):
                class_name = construct.__class__.__name__
                constraints = self.constraints_store.get(class_name, None)
                if constraints is not None and not isinstance(
                    construct, DataSpecificationIec61360
                ):
                    self.constraints_store[class_name].append(construct)

            if isinstance(construct.__class__, DataSpecificationIec61360):
                self.constraints_store["DataSpecificationIec61360"].append(construct)

            return cls.construct(args)

        parse_module.parse_concrete_object = aasc_3a_parse_concrete_object
