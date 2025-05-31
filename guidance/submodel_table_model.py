from dataclasses import asdict, dataclass, field
from typing import List, Optional


@dataclass
class RowModel:
    index: Optional[int] = None
    depth: Optional[int] = None
    model_type: Optional[str] = None
    id_short: Optional[str] = None
    _semantic_id: Optional[str] = field(init=False, default=None)
    _description: Optional[List[str]] = field(init=False, default=None)
    _value: Optional[str] = field(init=False, default=None)
    _value_type: Optional[str] = field(init=False, default=None)
    _reference_type: Optional[str] = None
    definition: Optional[str] = None

    @property
    def description(self) -> Optional[List[str]]:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if self._description is None:
            self._description = []
        self._description.append(value)

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
    def reference_type(self) -> Optional[str]:
        return self._reference_type

    @reference_type.setter
    def reference_type(self, value: str) -> None:
        if self._reference_type is None:
            self._reference_type = value

    @property
    def is_empty(self) -> bool:
        return not any(
            [
                self.id_short,
                self.model_type,
                self.depth,
            ]
        )

    def to_dict(self) -> dict:
        return {(k.lstrip("_")): v for k, v in asdict(self).items()}
