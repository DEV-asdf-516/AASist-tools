from enum import Enum
from typing import List, Optional
from aasist.src.module.tester.extends.extends_validation_context import (
    ExtendsValidationContext,
)
from aas_test_engines.test_cases.v3_0.parse import CheckConstraintException


class _LenientContextRules(Enum):
    allow_empty_string = "StringFormattedValue.__init__"
    xml_allow_empty_list = "XmlAdapter.as_list"
    json_allow_empty_list = "JsonAdapter.as_list"
    allow_none_list = "parse_list"
    allow_invalid_object = "parse_abstract_object"
    allow_missing_attribute_object = "parse_concrete_object"
    allow_empty_templates = "parse_submodel_templates"
    lenient_xml_env = "xml_to_env"
    lenient_json_env = "json_to_env"
    allow_empty_language_string_set = "LangStringSet.__init__"
    allow_empty_language = "LangStringSet.check_language"
    allow_empty_text = "LangStringSet.check_text"
    ignore_aasd_002 = "Referable.check_constraint_aasd_002"
    ignore_aasc_3a_008 = "ConceptDescription.check_aasc_3a_008"
    ignore_aasd_123 = "Reference.check_aasd_123"
    check_constraints = "check_constraints"


# 권장 제약조건 무시
class LenientValidationContext(ExtendsValidationContext):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        self._patch_check_constraints()
        self._patch_parse_submodel()
        self._patch_string_formatted_value()
        self._patch_as_list()
        self._patch_parse_list()
        self._patch_ignore_aasc_3a_008()
        self._patch_ignore_aasd_123()
        self._patch_ignore_aasd_002()
        self._patch_parse_object()
        self._patch_language_string_set()

    # StringFormattedValue
    def _patch_string_formatted_value(self):
        from aas_test_engines import reflect
        import re

        original_init = reflect.StringFormattedValue.__init__
        self.original_methods[_LenientContextRules.allow_empty_string.value] = (
            reflect.StringFormattedValue,
            "__init__",
            original_init,
        )

        def lenient_init(instance, raw_value: str):
            min_length: Optional[int] = getattr(instance, "min_length", None)
            max_length: Optional[int] = getattr(instance, "max_length", None)

            instance.raw_value = raw_value
            """
            Ignore:  String is shorter than 1 characters
            """
            if min_length is not None and min_length > 1:
                if len(raw_value) < instance.min_length:
                    raise ValueError(
                        f"String is shorter than {instance.min_length} characters"
                    )
            if max_length is not None:
                if len(raw_value) > instance.max_length:
                    raise ValueError(
                        f"String is longer than {instance.max_length} characters"
                    )

            # Constraint AASd-130: An attribute with data type "string" shall be restricted to the characters as defined in
            # XML Schema 1.0, i.e. the string shall consist of these characters only: ^[\x09\x0A\x0D\x20-\uD7FF\uE000-
            # \uFFFD\u00010000-\u0010FFFF]*$.
            if (
                re.fullmatch(
                    r"[\x09\x0a\x0d\x20-\ud7ff\ue000-\ufffd\U00010000-\U0010ffff]*",
                    raw_value,
                )
                is None
            ):
                raise ValueError(
                    "Constraint AASd-130 violated: String is not XML serializable"
                )

            if getattr(instance, "pattern", None) and len(raw_value) > 1:
                if re.fullmatch(instance.pattern, raw_value) is None:
                    raise ValueError(
                        f"String '{raw_value}' does not match pattern {instance.pattern}"
                    )

        reflect.StringFormattedValue.__init__ = lenient_init

    def _patch_as_list(self):
        """
        Ignore: Empty list not allowed
        """
        from aas_test_engines.test_cases.v3_0.adapter import (
            XmlAdapter,
            JsonAdapter,
            Adapter,
            AdapterException,
        )

        original_xml_as_list = XmlAdapter.as_list
        original_json_as_list = JsonAdapter.as_list

        self.original_methods[_LenientContextRules.xml_allow_empty_list.value] = (
            XmlAdapter,
            "as_list",
            original_xml_as_list,
        )
        self.original_methods[_LenientContextRules.json_allow_empty_list.value] = (
            JsonAdapter,
            "as_list",
            original_json_as_list,
        )

        def xml_lenient_as_list(instance, allow_empty: bool = True) -> List[Adapter]:
            result = []
            for idx, child in enumerate(instance.value):
                result.append(XmlAdapter(child, instance.path + idx))
            if not result and not allow_empty:
                return [XmlAdapter(value=instance.value, path=instance.path)]
            return result

        def json_lenient_as_list(instance, allow_empty: bool = True) -> List[Adapter]:
            if not isinstance(instance.value, list):
                raise AdapterException(f"Cannot convert {instance.value} to list")
            if not instance.value and not allow_empty:
                return [JsonAdapter(value=instance.value, path=instance.path)]
            return [
                JsonAdapter(val, instance.path + idx)
                for idx, val in enumerate(instance.value)
            ]

        XmlAdapter.as_list = xml_lenient_as_list
        JsonAdapter.as_list = json_lenient_as_list

    def _patch_parse_list(self):
        from aas_test_engines.test_cases.v3_0 import parse as parse_module
        from aas_test_engines.test_cases.v3_0.adapter import Adapter, AdapterException
        from aas_test_engines.reflect import ListType
        from aas_test_engines.result import AasTestResult, Level

        original_parse_list = parse_module.parse_list
        self.original_methods[_LenientContextRules.allow_none_list.value] = (
            parse_module,
            "parse_list",
            original_parse_list,
        )

        def lenient_parse_list(
            item_cls: ListType, value: Adapter, result: AasTestResult, allow_empty: bool
        ):
            parsed_list = []  # remove None
            try:
                items = value.as_list(allow_empty)
            except AdapterException as e:
                result.append(AasTestResult(f"{e} @ {value.path}", level=Level.ERROR))
                return parse_module.INVALID
            for item in items:
                if item is None:
                    continue
                obj = parse_module.parse(item_cls.item_type, item, result)
                if obj is None:
                    continue
                parsed_list.append(obj)
            return parsed_list

        parse_module.parse_list = lenient_parse_list

    def _patch_ignore_aasd_002(self):
        """
        Ignore: Constraint AASd-002
        """
        from aas_test_engines.test_cases.v3_0.model import Referable

        original_check_aasd_002 = Referable.check_constraint_aasd_002
        self.original_methods[_LenientContextRules.ignore_aasd_002.value] = (
            Referable,
            "check_constraint_aasd_002",
            original_check_aasd_002,
        )

        def lenient_check_aasd_002(instance):
            """
            Ignore: Constraint AASd-002
            """
            pass

        Referable.check_constraint_aasd_002 = lenient_check_aasd_002

    def _patch_ignore_aasc_3a_008(self):
        """
        Ignore: Constraint AASc-3a-008
        """
        from aas_test_engines.test_cases.v3_0.model import (
            ConceptDescription,
            DataSpecificationIec61360,
        )
        from aas_test_engines.data_types import is_bcp_47_for_english

        original_check_aasc_3a_008 = ConceptDescription.check_aasc_3a_008
        self.original_methods[_LenientContextRules.ignore_aasc_3a_008.value] = (
            ConceptDescription,
            "check_aasc_3a_008",
            original_check_aasc_3a_008,
        )

        def lenient_check_aasc_3a_008(instance):
            """
            Ignore: Constraint AASc-3a-008
            """
            if instance.embedded_data_specifications is None:
                return
            for idx, ds in enumerate(instance.embedded_data_specifications):
                """
                Ignore: skip checking if ds is an object
                """
                if isinstance(ds, object):
                    return
                if isinstance(ds.data_specification_content, DataSpecificationIec61360):
                    if ds.data_specification_content.value is not None:
                        continue
                    if ds.data_specification_content.definition is None:
                        raise CheckConstraintException(
                            f"Constraint AASc-3a-008 violated: embeddedDataSpecifications[{idx}].definition is missing"
                        )
                    if not any(
                        is_bcp_47_for_english(i.language)
                        for i in ds.data_specification_content.definition
                    ):
                        raise CheckConstraintException(
                            f"Constraint AASc-3a-008 violated: embeddedDataSpecifications[{idx}].definition.language is missing English."
                        )

        ConceptDescription.check_aasc_3a_008 = lenient_check_aasc_3a_008

    def _patch_ignore_aasd_123(self):
        """
        Ignore: Constraint AASd-123
        """
        from aas_test_engines.test_cases.v3_0.model import Reference, ReferenceType

        original_check_aasd_123 = Reference.check_aasd_123
        self.original_methods[_LenientContextRules.ignore_aasd_123.value] = (
            Reference,
            "check_aasd_123",
            original_check_aasd_123,
        )

        def lenient_check_aasd_123(instance):
            """
            Ignore: Constraint AASd-123
            """
            if instance.type != ReferenceType.ModelReference or instance.keys is None:
                return

        Reference.check_aasd_123 = lenient_check_aasd_123

    def _patch_parse_submodel(self):
        import importlib

        v3_0_module = importlib.import_module("aas_test_engines.test_cases.v3_0")
        from aas_test_engines.test_cases.v3_0 import parse as parse_module
        from aas_test_engines.test_cases.v3_0.adapter import AdapterPath
        from aas_test_engines.result import AasTestResult, Level
        from aas_test_engines.test_cases.v3_0.model import Environment
        from aas_test_engines.test_cases.v3_0 import parse_submodel as submodel_module
        from aas_test_engines.test_cases.v3_0 import (
            submodel_templates as template_module,
        )

        original_parse_submodel_templates = template_module.parse_submodel_templates
        self.original_methods[_LenientContextRules.allow_empty_templates.value] = (
            template_module,
            "parse_submodel_templates",
            original_parse_submodel_templates,
        )

        def lenient_parse_submodel_templates(
            root_result: AasTestResult, env: Environment
        ):
            """
            Ignore: Empty submodel templates
            """
            for submodel in env.submodels or []:
                try:
                    if isinstance(submodel, object):
                        return
                    if not submodel.semantic_id or not submodel.semantic_id.keys:
                        continue
                    sid = submodel.semantic_id.keys[0].value.raw_value
                    sub_result = AasTestResult(f"Check submodel '{submodel.id}'")
                    try:
                        template = template_module.templates[sid]
                    except KeyError:
                        sub_result.append(
                            AasTestResult(
                                f"Unknown semantic id '{sid}'", level=Level.WARNING
                            )
                        )
                        continue
                    sub_result.append(
                        AasTestResult(f"Template: {template.__name__} ({sid})")
                    )
                    parsed_submodel = submodel_module.parse_submodel(
                        sub_result, template, submodel
                    )
                    if sub_result.ok():
                        parse_module.check_constraints(
                            parsed_submodel, sub_result, AdapterPath()
                        )
                    root_result.append(sub_result)
                except AttributeError:
                    pass

        template_module.parse_submodel_templates = lenient_parse_submodel_templates
        v3_0_module.parse_submodel_templates = lenient_parse_submodel_templates

    def _patch_parse_object(self):
        from aas_test_engines.test_cases.v3_0 import parse as parse_module
        from aas_test_engines.reflect import ClassType
        from aas_test_engines.test_cases.v3_0.adapter import (
            Adapter,
            AdapterException,
        )
        from aas_test_engines.result import AasTestResult, Level

        original_parse_abstract_object = parse_module.parse_abstract_object
        original_parse_concrete_object = parse_module.parse_concrete_object

        self.original_methods[_LenientContextRules.allow_invalid_object.value] = (
            parse_module,
            "parse_abstract_object",
            original_parse_abstract_object,
        )
        self.original_methods[
            _LenientContextRules.allow_missing_attribute_object.value
        ] = (
            parse_module,
            "parse_concrete_object",
            original_parse_concrete_object,
        )

        def lenient_parse_concrete_object(
            cls: ClassType, adapter: Adapter, result: AasTestResult
        ):
            try:
                obj = adapter.as_object()
            except AdapterException as e:
                result.append(AasTestResult(f"{e} @ {adapter.path}", level=Level.ERROR))
                return None
            if parse_module.has_requires_model_type(cls.cls):
                try:
                    discriminator = adapter.get_model_type()
                    if discriminator != cls.cls.__name__:
                        result.append(
                            AasTestResult(
                                f"Wrong model type @ {adapter.path}", level=Level.ERROR
                            )
                        )
                except AdapterException as e:
                    result.append(
                        AasTestResult(
                            f"Model typ missing @ {adapter.path}", level=Level.ERROR
                        )
                    )

            args = {}
            all_fields = set()
            try:
                for field in cls.attrs:
                    field_name = field.force_name or parse_module.to_lower_camel_case(
                        field.name
                    )
                    all_fields.add(field_name)
                    try:
                        obj_value = obj[field_name]
                    except KeyError:
                        """
                        Ignore: Missing attribute
                        """
                        args[field.name] = None
                        continue

                    args[field.name] = parse_module.parse(field.type, obj_value, result)
            except TypeError as e:
                """
                Ignore: TypeError
                """
                return None

            return cls.construct(args)

        parse_module.parse_concrete_object = lenient_parse_concrete_object

        def lenient_parse_abstract_object(
            cls: ClassType, adapter: Adapter, result: AasTestResult
        ):
            try:
                discriminator = adapter.get_model_type()
            except AdapterException as e:
                result.append(
                    AasTestResult(f"{e} @ {adapter.path}", level=Level.WARNING)
                )
                return None
            subclass = None
            for subclass in cls.subclasses:
                if subclass.cls.__name__ == discriminator:
                    return lenient_parse_concrete_object(subclass, adapter, result)
            result.append(
                AasTestResult(
                    f"Invalid model type {discriminator} @ {adapter.path}",
                    level=Level.WARNING,
                )
            )
            return None

        parse_module.parse_abstract_object = lenient_parse_abstract_object

    def _patch_language_string_set(self):
        from aas_test_engines.test_cases.v3_0.model import LangStringSet

        original_check_language = LangStringSet.check_language
        original_check_text = LangStringSet.check_text
        allow_empty_language_string_set = LangStringSet.__init__

        self.original_methods[_LenientContextRules.allow_empty_language.value] = (
            LangStringSet,
            "check_language",
            original_check_language,
        )
        self.original_methods[_LenientContextRules.allow_empty_text.value] = (
            LangStringSet,
            "check_text",
            original_check_text,
        )
        self.original_methods[
            _LenientContextRules.allow_empty_language_string_set.value
        ] = (
            LangStringSet,
            "__init__",
            allow_empty_language_string_set,
        )

        def lenient_check_language(instance):
            """
            Ignore: Property 'language' must not be empty
            """
            pass

        def lenient_check_text(instance):
            """
            Ignore: Property 'text' must not be empty
            """
            text: str = getattr(instance, "text", None)
            if text is None:
                return
            if len(instance.text) > instance._max_len_text:
                raise CheckConstraintException(
                    f"Constraint violated: Property 'text' is too long ({len(text)} > {instance._max_len_text}"
                )

        def lenient_init(
            instance,
            max_len_text: int = 1024,
            language: str = "",
            text: str = "",
        ):

            instance.language = language
            instance.text = text
            instance._max_len_text = max_len_text

        LangStringSet.__init__ = lenient_init
        LangStringSet.check_language = lenient_check_language
        LangStringSet.check_text = lenient_check_text

    def _patch_ignore_aasd_114(self):
        """
        Ignore: Constraint AASd-114
        """
        from aas_test_engines.test_cases.v3_0.model import SubmodelElementList

        original_check_aasd_114 = SubmodelElementList.check_aasd_114
        self.original_methods[_LenientContextRules.ignore_aasd_114.value] = (
            SubmodelElementList,
            "check_aasd_114",
            original_check_aasd_114,
        )

        def lenient_check_aasd_114(instance):
            """
            Ignore: Constraint AASd-114
            """
            if not instance.value:
                return
            semantic_id = None
            for idx, el in enumerate(instance.value):
                if el is None:
                    continue
                if not el.semantic_id:
                    continue
                if semantic_id:
                    if el.semantic_id != semantic_id:
                        raise CheckConstraintException(
                            f"Constraint AASd-114 violated: Element {idx} must have semanticId {semantic_id} @ {self.id_short_path}"
                        )
                else:
                    semantic_id = el.semantic_id

        SubmodelElementList.check_aasd_114 = lenient_check_aasd_114

    def _patch_check_constraints(self):
        from aas_test_engines.test_cases.v3_0 import parse as parse_module
        from aas_test_engines.result import AasTestResult, Level

        original_check_constraints = parse_module.check_constraints
        self.original_methods[_LenientContextRules.check_constraints.value] = (
            parse_module,
            "check_constraints",
            original_check_constraints,
        )

        def lenient_check_constraints(
            obj, result: AasTestResult, path: Optional[str] = None
        ):
            """
            Ignore: Check constraints
            """
            if not parse_module.is_dataclass(obj):
                return

            fns = [(obj, getattr(obj, i)) for i in dir(obj) if i.startswith("check_")]
            for cls, fn in fns:
                try:
                    fn()
                except CheckConstraintException as e:
                    result.append(
                        AasTestResult(
                            f"""<{cls.__class__.__name__}>\n\r- {e} @ {path}""",
                            level=Level.ERROR,
                        )
                    )
                except AttributeError as e:
                    print(e)
            for field in parse_module.fields(obj):
                value = getattr(obj, field.name)
                if isinstance(value, list):
                    for idx, i in enumerate(value):
                        parse_module.check_constraints(
                            i, result, f"{path + '/' if path else ''}{field.name}/{idx}"
                        )
                else:
                    parse_module.check_constraints(
                        value, result, f"{path}/{field.name}"
                    )

        parse_module.check_constraints = lenient_check_constraints
