from typing import List
from aas_test_engines import result as te

from aasist.src.gui.handler import (
    _RESULT_LOG_NAME,
    LogLevel,
    QueueHandler,
)


class AasTestResultWrapper(te.AasTestResult):
    def __init__(
        self,
        message: str,
        level: te.Level = te.Level.INFO,
    ):
        super().__init__(message, level)
        self.level = level
        self.message = message
        self.sub_results: List[AasTestResultWrapper] = []
        self.logs = QueueHandler(_RESULT_LOG_NAME)
        self.logs.add(self.message, self._level_to_log_level())

    def to_logs(self):
        for sub_result in self.sub_results:
            yield from wrap_test_result(sub_result).to_logs()

    def _level_to_log_level(self) -> LogLevel:
        match self.level.value:
            case te.Level.INFO.value:
                return LogLevel.TRACE
            case te.Level.WARNING.value:
                return LogLevel.WARNING
            case te.Level.ERROR.value | te.Level.CRITICAL.value:
                return LogLevel.ERROR
            case _:
                return LogLevel.INFO


def wrap_test_result(result: te.AasTestResult) -> AasTestResultWrapper:
    if isinstance(result, AasTestResultWrapper):
        return result

    wrapper = AasTestResultWrapper.__new__(AasTestResultWrapper)

    for attr_name in dir(result):
        try:
            if attr_name.startswith("_"):
                continue
            attr_value = getattr(result, attr_name)
            if isinstance(attr_value, te.AasTestResult):
                wrapped = wrap_test_result(attr_value)
                setattr(wrapper, attr_name, wrapped)
            elif isinstance(attr_value, list):
                wrapped_collection = []
                for item in attr_value:
                    if isinstance(item, te.AasTestResult):
                        wrapped_collection.append(wrap_test_result(item))
                    else:
                        wrapped_collection.append(item)
                setattr(wrapper, attr_name, wrapped_collection)
            else:
                setattr(wrapper, attr_name, attr_value)
        except Exception as e:
            print(e)

    if hasattr(wrapper, "__init__"):
        try:
            wrapper.__init__(
                getattr(result, "message", ""), getattr(result, "level", None)
            )
        except:
            pass

    return wrapper
