from enum import Enum
from queue import Empty
import re
from typing import Dict
from aas_test_engines import file as te
import asyncio
from aasist.src.gui.handler import _TEST_LOG_NAME, LogLevel, QueueHandler
from aasist.src.module.format import AasFileFormat
from aasist.src.module.tester.extends.lenient_context import LenientValidationContext
from aasist.src.module.tester.option_type import IDTA
from aasist.src.module.tester.extends.test_result_wrapper import (
    AasTestResultWrapper,
    wrap_test_result,
)


class TestFileVerficator:
    def __init__(self, file: str, **kwargs):
        self._file = file
        self.use_aas_test_engine: bool = kwargs.get("use_aas_test_engine")
        self.ignore_opional_constraints: bool = kwargs.get(
            "ignore_optional_constraints"
        )
        self.results: Dict[Enum, bool] = {}
        self.log_handler = QueueHandler(_TEST_LOG_NAME)

    def verify(self):
        if self.use_aas_test_engine:
            if not self.ignore_opional_constraints:
                self._check_by_test_engine(self._file)
            else:
                with LenientValidationContext() as ctx:
                    self._check_by_test_engine(self._file)

        # TODO: KOSMO

    def _check_by_test_engine(self, file: str):
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
                        message, level = result.logs.get()
                        self.log_handler.add(message, level)
                        await asyncio.sleep(0.1)
                    except Empty:
                        break

            asyncio.run(_input_log())
            self.results[IDTA.standard] = result.ok()
        except FileNotFoundError:
            self.log_handler.add(f"{file} not found.", LogLevel.ERROR)
