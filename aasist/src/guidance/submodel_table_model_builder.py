from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from aasist.src.guidance.submodel_table_parser import ParseObject


class ModelBuilder(ABC):
    def __init__(
        self,
        current_instance: object | None = None,
        committed_instance: object | None = None,
        stage: Enum = None,
    ):
        self.current_instance: object | None = current_instance
        self.committed_instance: object | None = committed_instance
        self._stage: Enum = stage

    @abstractmethod
    def handle(self, object: ParseObject, **kwargs: Any):
        pass

    @abstractmethod
    def is_committed(self, object: ParseObject) -> bool:
        pass
