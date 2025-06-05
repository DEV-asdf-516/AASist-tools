from enum import Enum
from queue import Queue
import threading
from typing import Dict, Optional, Tuple


class LogLevel(Enum):
    TRACE = ("TRACE", "#000000")
    INFO = ("INFO", "#00AE09")
    SUCCESS = ("SUCCESS", "#0055FF")
    WARNING = ("WARNING", "#FF9800")
    ERROR = ("ERROR", "#FD1100")

    @property
    def color(self) -> str:
        return self.value[1]


_GUIDANCE_LOG_NAME = "GUIDANCE_OUTPUT"


class QueueHandler:

    _instances: Dict[str, "QueueHandler"] = {}
    _lock = threading.Lock()

    def __new__(cls, key: str, log_queue: Queue = Queue()):
        with cls._lock:
            if key not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[key] = instance
                instance._initialized = False
            return cls._instances[key]

    def __init__(self, key: str, log_queue: Queue = Queue()):
        if not self._initialized:
            self.key = key
            self.log_queue = log_queue
            self._initialized = True

    def _init_instance(self, log_queue: Queue):
        self.log_queue = log_queue

    def add(self, log: str, log_level: LogLevel = LogLevel.TRACE):
        self.log_queue.put((log, log_level))

    def get(self) -> Tuple[str, LogLevel]:
        return self.log_queue.get(block=False)

    @classmethod
    def get_handler(cls, key: str) -> Optional["QueueHandler"]:
        with cls._lock:
            return cls._instances[key]

    def clear(self):
        while not self.log_queue.empty():
            try:
                self.log_queue.get_nowait()
            except:
                break
