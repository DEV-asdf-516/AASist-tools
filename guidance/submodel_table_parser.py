from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    IO,
    Any,
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
)

from annotated_types import T

_P = TypeVar("_P", bound="ParseObject")


@dataclass(kw_only=True, slots=True)
class ParseObject(ABC, Generic[_P]):
    level: int
    children: Iterable[T] = field(default_factory=list)
    parent: Optional[T] = None

    @abstractmethod
    def __repr__(self) -> str:
        pass


class SubmodelTableParser(ABC):
    def __init__(self, file: IO, **kwargs: Any):
        self._file = file
        self._objects: Iterable[ParseObject] = []
        self._definitions: Iterable[ParseObject] = []
        self._root_submodels: List[str] = []

    @abstractmethod
    def parse_submodels(self, **kwargs: Any):
        pass
