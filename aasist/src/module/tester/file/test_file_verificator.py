from enum import Enum
from queue import Empty
import re
import threading
from typing import Dict
from aas_test_engines import file as te
import asyncio
from aasist.src.gui.handler import _TEST_LOG_NAME, LogLevel, QueueHandler
from aasist.src.module.format import AasFileFormat
from aasist.src.module.tester.extends.context.kosmo_validation_context import (
    KosmoValidationContext,
)
from aasist.src.module.tester.extends.context.lenient_validation_context import (
    LenientValidationContext,
)
from aasist.src.module.tester.constants import IDTA, CHECKLIST
from aasist.src.module.tester.extends.test_result_wrapper import (
    AasTestResultWrapper,
    wrap_test_result,
)
from aasist.src.module.tester.extends.registry.kosmo_validation_registry import (
    KosmoValidationRegistry,
)


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
            self.log_handler.add(f"{CHECKLIST[IDTA.standard]}", LogLevel.INFO)
            self._check_by_test_engine(self._file, IDTA.standard)

        if self.ignore_opional_constraints:
            self.log_handler.add("AAS Checklist options: IDTA", LogLevel.INFO)
            with LenientValidationContext() as ctx:  # TODO: AASX 뷰어 조회되면 pass
                self.log_handler.add(f"{CHECKLIST[IDTA.optional]}", LogLevel.INFO)
                # self._check_by_test_engine(self._file, IDTA.optional)

        if self.kosmo_options:
            self.log_handler.add("AAS Checklist options: KOSMO", LogLevel.INFO)

        with KosmoValidationContext() as ctx:
            registry: KosmoValidationRegistry = KosmoValidationRegistry(context=ctx)
            self._check_by_kosmo(self._file)
            for kosmo_option, enabled in self.kosmo_options.items():
                if not enabled:
                    continue
                if self.stop_event and self.stop_event.is_set():
                    return
                kosmo_validator = registry.get_validator(kosmo_option)
                if not kosmo_validator:
                    continue
                asyncio.run(kosmo_validator(registry))

            self.results.update(registry.results)

        self.log_handler.add("=========== [Test result] ===========")
        for checklist, ok in self.results.items():
            if ok:
                self.log_handler.add(
                    f"{CHECKLIST[checklist]}: Passed",
                    LogLevel.SUCCESS,
                )
            else:
                self.log_handler.add(
                    f"{CHECKLIST[checklist]}: Failed",
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
