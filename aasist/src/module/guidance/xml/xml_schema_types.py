from enum import Enum
from typing import Iterable, Union


_XML_KEY_MAP = {"aas": "https://admin-shell.io/aas/3/0"}
_AAS_KEY = "{" + _XML_KEY_MAP["aas"] + "}"


class XmlTags(Enum):
    KIND = "kind"
    TYPE = "type"
    ID_SHORT = "idShort"
    CATEGORY = "category"
    DISPLAY_NAME = "displayName"
    DESCRIPTION = "description"
    ADMINISTRATION = "administration"
    SEMANTIC_ID = "semanticId"
    SUPPLEMENTAL_SEMANTIC_IDS = "supplementalSemanticIds"
    REFERENCE = "reference"
    QUALIFIERS = "qualifiers"
    EMBEDDED_DATA_SPECIFICATIONS = "embeddedDataSpecifications"
    EXTENSIONS = "extensions"
    EXTENSION = "extension"
    FIRST = "first"
    SECOND = "second"
    KEYS = "keys"
    KEY = "key"
    VALUE = "value"
    REFERRED_SEMANTIC_ID = "referredSemanticId"
    REVISION = "revision"
    VERSION = "version"
    TEMPLATE_ID = "templateId"
    CREATOR = "creator"
    LANGUAGE = "language"
    TEXT = "text"
    LANG_STRING_NAME_TYPE = "langStringNameType"
    LANG_STRING_TEXT_TYPE = "langStringTextType"
    LANG_STRING_DEFINITION_TYPE_IEC_61360 = "langStringDefinitionTypeIec61360"
    LANG_STRING_PREFERRED_NAME_TYPE_IEC_61360 = "langStringPreferredNameTypeIec61360"
    LANG_STRING_SHORT_NAME_TYPE_IEC_61360 = "langStringShortNameTypeIec61360"
    VALUE_TYPE = "valueType"
    VALUE_ID = "valueId"
    REFERS_TO = "refersTo"
    ANNOTATED_RELATIONSHIP_ELEMENT = "annotatedRelationshipElement"
    BASIC_EVENT_ELEMENT = "basicEventElement"
    CAPABILITY = "capability"
    ENTITY = "entity"
    OPERATION = "operation"
    RELATIONSHIP_ELEMENT = "relationshipElement"
    SUBMODEL_ELEMENT_COLLECTION = "submodelElementCollection"
    SUBMODEL_ELEMENT_LIST = "submodelElementList"
    BLOB = "blob"
    FILE = "file"
    MULTI_LANGUAGE_PROPERTY = "multiLanguageProperty"
    PROPERTY = "property"
    RANGE = "range"
    REFERENCE_ELEMENT = "referenceElement"
    ANNOTATIONS = "annotations"
    OBSERVED = "observed"
    DIRECTION = "direction"
    STATE = "state"
    MESSAGE_TOPIC = "messageTopic"
    MESSAGE_BROKER = "messageBroker"
    LAST_UPDATE = "lastUpdate"
    MIN_INTERVAL = "minInterval"
    MAX_INTERVAL = "maxInterval"
    CONTENT_TYPE = "contentType"
    SPECIFIC_ASSET_IDS = "specificAssetIds"
    ENTITY_TYPE = "entityType"
    GLOBAL_ASSET_ID = "globalAssetId"
    STATEMENTS = "statements"
    PATH = "path"
    INPUT_VARIABLES = "inputVariables"
    OUTPUT_VARIABLES = "outputVariables"
    INOUTPUT_VARIABLES = "inoutputVariables"
    OPERATION_VARIABLES = "operationVariables"
    MAX = "max"
    MIN = "min"
    TYPE_VALUE_LIST_ELEMENT = "typeValueListElement"
    ORDER_RELEVANT = "orderRelevant"
    SEMANTIC_ID_LIST_ELEMENT = "semanticIdListElement"
    VALUE_TYPE_LIST_ELEMENT = "valueTypeListElement"
    ASSET_INFORMATION = "assetInformation"
    DERIVED_FROM = "derivedFrom"
    NAME = "name"
    EXTERNAL_SUBJECT_ID = "externalSubjectId"
    ASSET_KIND = "assetKind"
    ASSET_TYPE = "assetType"
    DEFAULT_THUMBNAIL = "defaultThumbnail"
    ID = "id"
    SUBMODEL_ELEMENTS = "submodelElements"
    VALUE_REFERENCE_PAIRS = "valueReferencePairs"
    VALUE_REFERENCE_PAIR = "valueReferencePair"
    IS_CASE_OF = "isCaseOf"
    DATA_SPECIFICATION_CONTENT = "dataSpecificationContent"
    DATA_SPECIFICATION = "dataSpecification"
    PREFERRED_NAME = "preferredName"
    SHORT_NAME = "shortName"
    UNIT = "unit"
    UNIT_ID = "unitId"
    SOURCE_OF_DEFINITION = "sourceOfDefinition"
    SYMBOL = "symbol"
    DATA_TYPE = "dataType"
    DEFINITION = "definition"
    VALUE_FORMAT = "valueFormat"
    VALUE_LIST = "valueList"
    LEVEL_TYPE = "levelType"
    ASSET_ADMINISTRATION_SHELL = "assetAdministrationShell"
    ASSET_ADMINISTRATION_SHELLS = "assetAdministrationShells"
    CONCEPT_DESCRIPTION = "conceptDescription"
    CONCEPT_DESCRIPTIONS = "conceptDescriptions"
    SUBMODEL = "submodel"
    SUBMODELS = "submodels"

    @classmethod
    def is_match(
        cls,
        tag: str,
        check: Union["XmlTags", Iterable["XmlTags"]],
        prefix: str = _AAS_KEY,
    ) -> bool:
        if tag is None:
            return False
        stripped = tag.replace(prefix, "")
        try:
            if isinstance(check, XmlTags):
                return stripped == check.value
            if isinstance(check, Iterable):
                return any(stripped == item.value for item in check)
        except TypeError:
            return False
