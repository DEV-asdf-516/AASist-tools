from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import (
    IO,
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
)

from annotated_types import T

_P = TypeVar("_P", bound="ParseObject")


@dataclass(init=False)
class ParseObjectIdentifier:
    id: str
    id_short: str


@dataclass(kw_only=True, slots=True)
class ParseObject(ABC, Generic[_P]):
    level: int
    children: Iterable[T] = field(default_factory=list)
    parent: Optional[T] = None

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


class SubmodelTableParser(ABC):
    def __init__(self, file: IO, **kwargs: Any):
        self._file = file
        self._objects: Iterable[ParseObject] = []
        self._definitions: Iterable[ParseObject] = []
        self._submodel_identifiers: Dict[str : List[ParseObjectIdentifier]] = {}

    @abstractmethod
    def parse_submodels(self, **kwargs: Any):
        pass
