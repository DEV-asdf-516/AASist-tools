from enum import Enum
from typing import Dict, Iterable, List, Optional
from aasist.src.module.tester.extends.context.extends_validation_context import (
    ExtendsValidationContext,
)
from aas_test_engines.test_cases.v3_0.model import (
    Referable,
    Identifiable,
    AssetInformation,
)


class _KosmoContextRules(Enum):
    parse_concrete_object = "parse_concrete_object"
    aasd_002 = "Referable.check_constraint_aasd_002"
    aasd_007 = "Property.check_aasd_007"
    aasd_117 = "ensure_have_id_shorts"
    aasc_3a_008 = "ConceptDescription.check_aasc_3a_008"


class KosmoValidationContext(ExtendsValidationContext):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        self.referables: Dict[str, List[Referable]] = {
            "AssetAdministrationShell": [],
            "Submodel": [],
            "SubmodelElementCollection": [],
            "Property": [],
            "ConceptDescription": [],
        }
        self.identifiables: Dict[str, List[Identifiable]] = {
            "AssetAdministrationShell": [],
            "Submodel": [],
            "ConceptDescription": [],
        }
        self.asset_informations: List[AssetInformation] = []
        self._petch_parse()
        self._petch_kosmo_id_short_rules()
        self._patch_kosmo_concept_description_rules()
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
        self.original_methods[_KosmoContextRules.parse_concrete_object.value] = (
            parse_module,
            "parse_concrete_object",
            original_parse_concrete_object,
        )

        def kosmo_parse_concrete_object(
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

            # idShort rule - 명명규칙 / Submodel 구성요소 검사
            if issubclass(construct.__class__, Referable) and getattr(
                construct.id_short, "raw_value", None
            ):
                class_name = construct.__class__.__name__
                referables = self.referables.get(class_name, None)
                if referables is not None:
                    self.referables[class_name].append(construct)
            # IRDI/IRI 형식 검사
            if issubclass(construct.__class__, Identifiable):
                class_name = construct.__class__.__name__
                identifiables = self.identifiables.get(class_name, None)
                if identifiables is not None:
                    self.identifiables[class_name].append(construct)
            # globalAssetId 검사
            if isinstance(construct, AssetInformation):
                self.asset_informations.append(construct)

            return cls.construct(args)

        parse_module.parse_concrete_object = kosmo_parse_concrete_object

    def _petch_kosmo_id_short_rules(self):
        from aas_test_engines.test_cases.v3_0 import model as model_module
        from aas_test_engines.test_cases.v3_0.model import Referable, IdShortPath
        import re

        original_check_aasd_002 = Referable.check_constraint_aasd_002
        self.original_methods[_KosmoContextRules.aasd_002.value] = (
            Referable,
            "check_constraint_aasd_002",
            original_check_aasd_002,
        )
        original_ensure_have_id_shorts = model_module.ensure_have_id_shorts
        self.original_methods[_KosmoContextRules.aasd_117.value] = (
            model_module,
            "ensure_have_id_shorts",
            original_ensure_have_id_shorts,
        )

        def kosmo_id_short_naming_rule(instance) -> Optional[str]:
            if hasattr(instance, "id_short") and hasattr(
                instance.id_short, "raw_value"
            ):
                if (
                    re.fullmatch(r"[A-Z][a-zA-Z0-9_]*", instance.id_short.raw_value)
                    is None
                ):
                    return f"""The idShort "{instance.id_short}" violates the Kosmo rules:\n\r- idShort는 비어있을 수 없습니다.\n\r- idShort는 반드시 영문 대문자로 시작해야 합니다.\n\r- idShort는 영문 대소문자, 숫자, 밑줄(_)만 포함할 수 있습니다."""

        def kosmo_id_short_exist_rule(
            elements: Optional[List["Referable"]],
            id_short_path: Optional[IdShortPath] = None,
        ) -> Optional[str]:
            if elements is None:
                return
            if not isinstance(elements, Iterable):
                elements = [elements]
            for val in elements:
                if not isinstance(val, Referable):
                    continue
                if val.id_short is None:
                    msg = f"""The "{val.__class__}" violates the Kosmo rules:\n\r- 다음 항목에 대해 반드시 idShort가 설정되어야 합니다.\n\t1) AssetAdministrationShell\n\t2) Submodel\n\t3) SubmodelElementCollection\n\t4) ConceptDescription\n\t5) Property"""
                    return msg

        model_module.ensure_have_id_shorts = kosmo_id_short_exist_rule
        Referable.check_constraint_aasd_002 = kosmo_id_short_naming_rule

    def _patch_kosmo_concept_description_rules(self):
        from aas_test_engines.test_cases.v3_0.model import (
            ConceptDescription,
            DataSpecificationIec61360,
        )

        original_check_aasc_3a_008 = ConceptDescription.check_aasc_3a_008
        self.original_methods[_KosmoContextRules.aasc_3a_008.value] = (
            ConceptDescription,
            "check_aasc_3a_008",
            original_check_aasc_3a_008,
        )

        def kosmo_definition_rule(instance) -> Optional[str]:
            if instance.embedded_data_specifications is None:
                return
            if instance.description:
                return
            for ds in instance.embedded_data_specifications:
                if isinstance(ds.data_specification_content, DataSpecificationIec61360):
                    if ds.data_specification_content.value is not None:
                        continue
                    if ds.data_specification_content.definition is None:
                        return f"""The ConceptDescription "{instance.id_short}" violates the Kosmo rules:\n\r- description/definition이 누락되었습니다."""

        ConceptDescription.check_aasc_3a_008 = kosmo_definition_rule
