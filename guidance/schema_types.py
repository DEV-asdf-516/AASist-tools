from enum import Enum, auto


class TableFormat(Enum):
    XLSX = ".xlsx"
    DOCX = ".docx"


class AasFileFormat(Enum):
    JSON = "json"
    XML = "xml"
    AASX = "aasx"


class ParentElement(Enum):
    SUBMODEL_ELEMENT_COLLECTION = ("submodelElementCollection", "SMC")
    ENTITY = ("entity", "Ent")
    SUBMODEL_ELEMENT_LIST = ("submodelElementList", "ElementList")
    OPERATION = ("operation", "Opr")
    RELATIONSHIP_ELEMENT = ("relationshipElement", "Rel")
    BASIC_EVENT_ELEMENT = ("basicEventElement", "Evt")
    ANNOTATED_RELATIONSHIP_ELEMENT = ("annotatedRelationshipElement", "RelA")

    @classmethod
    def contains(cls, value: str) -> bool:
        value = value.lower()
        return any(
            value == full.lower() or value.lower() == short.lower()
            for full, short in (e.value for e in cls)
        )


# Extracted from: package-explorer/src/AasxCsharpLibrary/AasxCompatibilityModels/V20/AdminShell.cs
SIMPLE_MODEL_TYPES = {
    "Referable": "Ref",
    "Reference": "Rfc",
    "AssetAdministrationShellRef": "AasRef",
    "AssetRef": "AssetRef",
    "SubmodelRef": "SMRef",
    "ConceptDescriptionRef": "CDRef",
    "DataSpecificationRef": "DSRef",
    "ContainedElementRef": "CERef",
    "AssetAdministrationShells": "AASs",
    "Assets": "Assets",
    "Submodels": "SMS",
    "ConceptDescriptions": "CDS",
    "AdministrationShellEnv": "Env",
    "AssetAdministrationShell": "AAS",
    "Asset": "Asset",
    "View": "View",
    "ConceptDescription": "CD",
    "ConceptDictionary": "CDic",
    "Submodel": "SM",
    "Qualifier": "Qfr",
    "OperationVariable": "OprVar",
    "SubmodelElement": "SME",
    "DataElement": "DE",
    "Property": "Prop",
    "MultiLanguageProperty": "MLP",
    "Range": "Range",
    "Blob": "Blob",
    "File": "File",
    "ReferenceElement": "Ref",
    "RelationshipElement": "Rel",
    "AnnotatedRelationshipElement": "RelA",
    "Capability": "Cap",
    "SubmodelElementCollection": "SMC",
    "Operation": "Opr",
    "Entity": "Ent",
    "BasicEvent": "Evt",
    # etc
    "SubmodelElementList": "ElementList",
}
