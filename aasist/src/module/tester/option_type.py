from enum import Enum, auto


class IDTA(Enum):
    standard = auto()
    optional = auto()


class KOSMO(Enum):
    id_short_rule = auto()
    id_rule = auto()
    submodel_rule = auto()
    concept_description_rule = auto()
    kind_rule = auto()
    thumbnail_rule = auto()
    value_rule = auto()
    submodel_element_collection_rule = auto()
