from dataclasses import dataclass
from enum import Enum
from queue import Empty
import re
import threading
from typing import Dict
from aas_test_engines import file as te
import asyncio
from aasist.src.gui.handler import _TEST_LOG_NAME, LogLevel, QueueHandler
from aasist.src.module.format import AasFileFormat
from aasist.src.module.tester.extends.context.aasc_3a_validation_context import (
    Aasc3aValidationContext,
)
from aasist.src.module.tester.extends.context.aasd_validation_context import (
    AasdValidationContext,
)
from aasist.src.module.tester.extends.context.extends_validation_context import (
    ExtendsValidationContext,
)
from aasist.src.module.tester.extends.context.kosmo_validation_context import (
    KosmoValidationContext,
)
from aasist.src.module.tester.extends.context.lenient_validation_context import (
    LenientValidationContext,
)
from aasist.src.module.tester.constants import IDTA, CHECKLIST
from aasist.src.module.tester.extends.registry.aasc_3a_validation_registry import (
    Aasc3aValidationRegistry,
)
from aasist.src.module.tester.extends.registry.aasd_validation_registry import (
    AasdValidationRegistry,
)
from aasist.src.module.tester.extends.registry.validation_registry import (
    ValidationRegistry,
)
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
        self.idta_options: Dict[str, bool] = kwargs.get("idta_options", {})
        self.kosmo_options: Dict[str, bool] = kwargs.get("kosmo_options", {})
        self.results: Dict[str, bool] = {}
        self.log_handler = QueueHandler(_TEST_LOG_NAME)
        self.stop_event: threading.Event = kwargs.get("stop_event", None)

    def verify(self):
        self.log_handler.add("=========== [Test start] ===========")
        self.log_handler.add(f"Testing file: {self._file}")

        if self.idta_options:
            self.log_handler.add("AAS Checklist options: IDTA", LogLevel.INFO)

        standard_idta_options = {
            k: v
            for k, v in self.idta_options.items()
            if k in [IDTA.standard.name, IDTA.optional.name]
        }

        if standard_idta_options:
            for idta_option, enabled in standard_idta_options.items():
                if not enabled:
                    continue
                if self.stop_event and self.stop_event.is_set():
                    return
                self.log_handler.add(f"{CHECKLIST[idta_option]}", LogLevel.INFO)
                if idta_option == IDTA.standard.name:
                    self._check_with_detail_log(self._file, IDTA.standard)
                if idta_option == IDTA.optional.name:
                    with LenientValidationContext() as ctx:  # TODO: AASX 뷰어 조회되면 pass
                        # self._check_with_detail_log(self._file, IDTA.optional)
                        pass

        aasd_idta_constraints_options = {
            k: v for k, v in self.idta_options.items() if "aasd" in k
        }

        if aasd_idta_constraints_options:
            self._execute_register(
                options=aasd_idta_constraints_options,
                context=AasdValidationContext,
                registry=AasdValidationRegistry,
            )

        aasc_3a_idta_constraints_options = {
            k: v for k, v in self.idta_options.items() if "aasc_3a" in k
        }

        if aasc_3a_idta_constraints_options:
            self._execute_register(
                options=aasc_3a_idta_constraints_options,
                context=Aasc3aValidationContext,
                registry=Aasc3aValidationRegistry,
            )

        if self.kosmo_options:
            self.log_handler.add("AAS Checklist options: KOSMO", LogLevel.INFO)
            self._execute_register(
                options=self.kosmo_options,
                context=KosmoValidationContext,
                registry=KosmoValidationRegistry,
            )

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

    def _execute_register(
        self,
        options: Dict[str, bool],
        context: ExtendsValidationContext,
        registry: ValidationRegistry,
    ):
        if not options:
            return

        with context() as ctx:
            registry: ValidationRegistry = registry(context=ctx)
            self._check(self._file)
            for option, enabled in options.items():
                if not enabled:
                    continue
                if self.stop_event and self.stop_event.is_set():
                    return
                validator = registry.get_validator(option)
                if not validator:
                    continue
                asyncio.run(validator(registry))

            self.results.update(registry.results)

    def _check_with_detail_log(self, file: str, checklist: Enum):
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
            self.results[checklist.name] = result.ok()
        except FileNotFoundError:
            self.log_handler.add(f"{file} not found.", LogLevel.ERROR)

    def _check(self, file: str):
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
