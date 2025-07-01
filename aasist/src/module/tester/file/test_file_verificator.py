from enum import Enum
from queue import Empty
import re
import threading
from typing import Dict, List, Union
from aas_test_engines import file as te
from aas_test_engines.reflect import TypeBase
import asyncio
from aasist.src.gui.handler import _TEST_LOG_NAME, LogLevel, QueueHandler
from aasist.src.module.format import AasFileFormat
from aasist.src.module.tester.extends.kosmo_validation_context import (
    KosmoValidationContext,
)
from aasist.src.module.tester.extends.lenient_validation_context import (
    LenientValidationContext,
)
from aasist.src.module.tester.option_type import IDTA, KOSMO
from aasist.src.module.tester.extends.test_result_wrapper import (
    AasTestResultWrapper,
    wrap_test_result,
)

_CHECKLIST = {
    IDTA.standard: "# 1. 표준 검사",
    IDTA.optional: "# 2. 느슨한 표준 검사",
    KOSMO.id_short_rule: "# 1. idShort 설정/명명 규칙 검사",
    KOSMO.id_rule: "# 2. IRDI/IRI 형식 검사",
    KOSMO.submodel_rule: "# 3. Submodel 구성 검사",
    KOSMO.concept_description_rule: "# 4. ConceptDescription 규칙 검사",
    KOSMO.kind_rule: "# 5. Kind 유형 검사",
    KOSMO.thumbnail_rule: "# 6. Thumbnail 이미지 확인",
    KOSMO.value_rule: "# 7. Value 값 존재 여부 확인",
    KOSMO.submodel_element_collection_rule: "# 8. Concept Description mapping 확인",
}


class TestFileVerficator:

    def __init__(self, file: str, **kwargs):
        self._file = file
        self.use_aas_test_engine: bool = kwargs.get("use_aas_test_engine")
        self.ignore_opional_constraints: bool = kwargs.get(
            "ignore_optional_constraints"
        )
        self.kosmo_options: Dict[str, bool] = kwargs.get("kosmo_options", {})
        self.results: Dict[Enum, bool] = {}
        self.log_handler = QueueHandler(_TEST_LOG_NAME)
        self.stop_event: threading.Event = kwargs.get("stop_event", None)

    def verify(self):
        self.log_handler.add("=========== [Test start] ===========")
        self.log_handler.add(f"Testing file: {self._file}")

        if self.use_aas_test_engine:
            self.log_handler.add("AAS Checklist options: IDTA", LogLevel.INFO)
            self.log_handler.add(f"{_CHECKLIST[IDTA.standard]}", LogLevel.INFO)
            self._check_by_test_engine(self._file, IDTA.standard)

        if self.ignore_opional_constraints:
            self.log_handler.add("AAS Checklist options: IDTA", LogLevel.INFO)
            with LenientValidationContext():  # TODO: 권장 제약옵션만
                self.log_handler.add(f"{_CHECKLIST[IDTA.optional]}", LogLevel.INFO)
                self._check_by_test_engine(self._file, IDTA.optional)

        if self.kosmo_options:
            self.log_handler.add("AAS Checklist options: KOSMO", LogLevel.INFO)

        for kosmo_option, enabled in self.kosmo_options.items():
            if not enabled:
                continue
            if self.stop_event and self.stop_event.is_set():
                return
            with KosmoValidationContext() as ctx:
                self._check_by_kosmo(self._file)
                if kosmo_option == KOSMO.id_short_rule.name:
                    asyncio.run(self._check_kosmo_id_short_rule(context=ctx))
                if kosmo_option == KOSMO.id_rule.name:
                    pass
                if kosmo_option == KOSMO.submodel_rule.name:
                    asyncio.run(self._check_kosmo_submodel_component_rule(context=ctx))
                if kosmo_option == KOSMO.concept_description_rule.name:
                    asyncio.run(self._check_kosmo_concept_description_rule(context=ctx))
                if kosmo_option == KOSMO.kind_rule.name:
                    pass
                if kosmo_option == KOSMO.thumbnail_rule.name:
                    pass
                if kosmo_option == KOSMO.submodel_element_collection_rule.name:
                    pass

        self.log_handler.add("=========== [Test result] ===========")
        for checklist, ok in self.results.items():
            if ok:
                self.log_handler.add(
                    f"{checklist.__class__.__name__} {_CHECKLIST[checklist]}: Passed",
                    LogLevel.SUCCESS,
                )
            else:
                self.log_handler.add(
                    f"{checklist.__class__.__name__} {_CHECKLIST[checklist]}: Failed",
                    LogLevel.ERROR,
                )

    def _check_by_test_engine(self, file: str, checklist: Enum):
        extension = re.sub(r".*\.", "", file)
        result: AasTestResultWrapper = None

        try:
            with open(file, "rb") as f:
                if extension == AasFileFormat.AASX.value:
                    result = te.check_aasx_file(f)
                if extension == AasFileFormat.XML.value:
                    result = te.check_xml_file(f)
                if extension == AasFileFormat.JSON.value:
                    result = te.check_json_file(f)

            result = wrap_test_result(result)

            async def _input_log():
                for _ in result.to_logs():
                    await asyncio.sleep(0.1)
                while True:
                    try:
                        if self.stop_event and self.stop_event.is_set():
                            self.log_handler.add("Test stopped!", LogLevel.INFO)
                            result.logs.clear()
                            break
                        message, level = result.logs.get()
                        self.log_handler.add(message, level)
                        await asyncio.sleep(0.1)
                    except Empty:
                        break

            asyncio.run(_input_log())
            self.results[checklist] = result.ok()
        except FileNotFoundError:
            self.log_handler.add(f"{file} not found.", LogLevel.ERROR)

    def _check_by_kosmo(self, file: str):
        extension = re.sub(r".*\.", "", file)
        try:
            with open(file, "rb") as f:
                if extension == AasFileFormat.AASX.value:
                    te.check_aasx_file(f)
                if extension == AasFileFormat.XML.value:
                    te.check_xml_file(f)
                if extension == AasFileFormat.JSON.value:
                    te.check_json_file(f)
        except FileNotFoundError:
            self.log_handler.add(f"{file} not found.", LogLevel.ERROR)

    async def _check_kosmo_id_short_rule(self, context: KosmoValidationContext):
        self.results[KOSMO.id_short_rule] = True
        self.log_handler.add(f"{_CHECKLIST[KOSMO.id_short_rule]}", LogLevel.INFO)

        await self._check_kosmo_rule_with_logging(
            context.parents, "check_aasd_117", KOSMO.id_short_rule
        )
        await self._check_kosmo_rule_with_logging(
            context.referables, "check_constraint_aasd_002", KOSMO.id_short_rule
        )

    async def _check_kosmo_submodel_component_rule(
        self, context: KosmoValidationContext
    ):
        require_components = [
            "Identification",
            "TechnicalData",
            "Documentation",
            "OperationalData",
        ]
        self.log_handler.add(f"{_CHECKLIST[KOSMO.submodel_rule]}", LogLevel.INFO)
        id_shorts = [ref.id_short.raw_value for ref in context.referables]
        all_included = set(require_components).issubset(set(id_shorts))
        self.results[KOSMO.submodel_rule] = all_included
        if not all_included:
            missing = set(require_components) - set(id_shorts)
            self.log_handler.add(
                f"""The Submodel violates the Kosmo rules:\n\r- 필수 서브모델 {', '.join(missing)}이(가) 누락되었습니다.""",
                LogLevel.ERROR,
            )
            self.results[KOSMO.submodel_rule] = False

    async def _check_kosmo_concept_description_rule(
        self, context: KosmoValidationContext
    ):
        self.results[KOSMO.concept_description_rule] = True
        self.log_handler.add(
            f"{_CHECKLIST[KOSMO.concept_description_rule]}", LogLevel.INFO
        )
        await self._check_kosmo_rule_with_logging(
            context.concept_descriptions,
            "check_aasc_3a_008",
            KOSMO.concept_description_rule,
        )

    async def _check_kosmo_rule_with_logging(
        self, objects: List[TypeBase], method_name: Union[str, List[str]], rule: KOSMO
    ):
        for obj in objects:
            if hasattr(obj, method_name) is False:
                continue
            message = getattr(obj, method_name)()
            if not message:
                continue
            self.log_handler.add(
                message,
                log_level=LogLevel.ERROR,
            )
            await asyncio.sleep(0.1)
            self.results[rule] = False
