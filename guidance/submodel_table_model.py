from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RowModel:
    index: Optional[int] = None
    depth: Optional[int] = None
    model_type: Optional[str] = None
    id_short: Optional[str] = None
    _semantic_id: Optional[str] = field(init=False, default=None)
    _definition: Optional[List[str]] = field(init=False, default=None)
    _value: Optional[str] = field(init=False, default=None)
    _value_type: Optional[str] = field(init=False, default=None)

    @property
    def definition(self) -> Optional[List[str]]:
        return self._definition

    @definition.setter
    def definition(self, value: str) -> None:
        if self._definition is None:
            self._definition = []
        self._definition.append(value)

    @property
    def value(self) -> Optional[str]:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

    @property
    def value_type(self) -> Optional[str]:
        return self._value_type

    @value_type.setter
    def value_type(self, value: str) -> None:
        self._value_type = value

    @property
    def semantic_id(self) -> Optional[str]:
        return self._semantic_id

    @semantic_id.setter
    def semantic_id(self, value: str) -> None:
        if self._semantic_id is None:
            self._semantic_id = value

    @property
    def is_empty(self) -> bool:
        return not any(
            [
                self.id_short,
                self.model_type,
                self.depth,
            ]
        )
