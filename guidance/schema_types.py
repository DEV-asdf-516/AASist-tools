from enum import Enum, auto


class TableFormat(Enum):
    XLSX = auto()
    DOCX = auto()


class AasFileFormat(Enum):
    JSON = "json"
    XML = "xml"
    AASX = "aasx"


class TableAttributes(Enum):
    SMC = auto()
    ID_SHORT = auto()
    SEMANTIC_ID = auto()
    DEFINITION = auto()
    VALUE = auto()
    VALUE_TYPE = auto()
    MODEL_TYPE = auto()


class ParentElement(Enum):
    SUBMODEL_ELEMENT_COLLECTION = "submodelElementCollection"
    ENTITY = "entity"
    SUBMODEL_ELEMENT_LIST = "submodelElementList"
    OPERATION = "operation"
    RELATIONSHIP_ELEMENT = "relationshipElement"
    BASIC_EVENT_ELEMENT = "basicEventElement"
    ANNOTATED_RELATIONSHIP_ELEMENT = "annotatedRelationshipElement"

    @classmethod
    def contains(cls, value: str) -> bool:
        return value.lower() in _PARENTS_TYPES


_PARENTS_TYPES = {
    submodel_element_type.value.lower(): submodel_element_type
    for submodel_element_type in ParentElement
}

_SIMPLE_MODEL_TYPES = {
    "property": "Prop",
    "multiLanguageProperty": "MLP",
    "submodelElementCollection": "SMC",
    "submodelElementList": "ElementList",
    "entity": "ENT",
    "relationshipElement": "Rel",
    "file": "File",
    "range": "Range",
}
