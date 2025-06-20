from enum import Enum
from typing import Any, Dict, Optional


class _LenientContextRules(Enum):
    allow_empty_string = "StringFormattedValue.__init__"
    xml_allow_empty_list = "XmlAdapter.as_list"


# 권장 제약조건 무시
class LenientValidationContext:
    def __init__(self):
        self.original_methods: Dict[str, Any] = {}

    def __enter__(self):
        self._patch_string_formatted_value()
        self._patch_as_list()

    def __exit__(self, exc_type, exc_val, traceback):
        self._restore_patched_methods()
        return False

    def _restore_patched_methods(self):
        for (
            target_class,
            method_name,
            original_method,
        ) in self.original_methods.values():
            setattr(target_class, method_name, original_method)
        self.original_methods.clear()

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

                if getattr(instance, "pattern", None):
                    if re.fullmatch(instance.pattern, raw_value) is None:
                        raise ValueError(
                            f"String '{raw_value}' does not match pattern {instance.pattern}"
                        )

        reflect.StringFormattedValue.__init__ = lenient_init

    def _patch_as_list(self):
        print("Patching XmlAdapter.as_list to allow empty lists")
        from aas_test_engines.test_cases.v3_0.adapter import XmlAdapter

        # TODO
