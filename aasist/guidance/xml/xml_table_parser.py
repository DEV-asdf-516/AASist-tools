import copy
import logging
from typing import IO, Any, Callable, Dict, Iterable, List, Optional, Tuple
from lxml import etree
from gui.handler import _GUIDANCE_LOG_NAME, QueueHandler
from guidance.submodel_table_parser import (
    ParseObject,
    ParseObjectIdentifier,
    SubmodelTableParser,
)
from guidance.xml.xml_schema_types import _AAS_KEY, XmlTags


logger = logging.getLogger(__name__)


class XmlDataObject(ParseObject):
    def __init__(self, element: etree._Element, level: int = 0, index: int = 0):
        super().__init__(
            level=level,
            children=list(element),
        )
        self.index = index
        self.element = element
        self.tag = element.tag
        self.text = element.text
        self.parent: Optional[etree._Element] = element.getparent()

    def __repr__(self):
        return f"""{"-" * self.level}> XmlObject(index={self.index}, level={self.level}, tag={self.tag}, text={self.text}, parent={self.parent.tag})"""

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, XmlDataObject):
            return False
        return (
            self.tag == other.tag
            and self.text == other.text
            and self.level == other.level
            and self.parent is other.parent
        )

    def __hash__(self) -> int:
        if not hasattr(self, "_cached_hash"):
            self._cached_hash = hash(
                (
                    self.tag,
                    self.text,
                    self.level,
                    id(self.parent) if self.parent else None,
                )
            )
        return self._cached_hash


class XmlTableParser(SubmodelTableParser):

    def __init__(self, file: IO):
        super().__init__(file=file)
        self.bin: IO = file
        self._objects: List[XmlDataObject] = []
        self._definitions: List[XmlDataObject] = []
        self._submodel_identifiers: Dict[str : List[ParseObjectIdentifier]] = {}

    def parse_submodels(self, **kwargs: Any):
        self._objects: List[XmlDataObject] = []
        self._root_submodels: List[str] = []

        document = self.parse_xml()

        if document is None:
            logger.error("failed to parse xml")
            return None

        submodel_elements: List[XmlDataObject] = []
        concept_description_elements: List[XmlDataObject] = []

        aas_submodels = document.find(_AAS_KEY + XmlTags.SUBMODELS.value)

        # just for logging
        log_handler = QueueHandler(_GUIDANCE_LOG_NAME)
        aas_shells = document.find(_AAS_KEY + XmlTags.ASSET_ADMINISTRATION_SHELLS.value)

        for _, aas in self._find_elements_by_condition(
            aas_shells, lambda e: XmlTags.is_match(e.tag, XmlTags.ID_SHORT)
        ):
            aas: etree._Element
            log_handler.add(f"Assemble asset Administration Shell...: {aas.text}")

        # set submodel identifier
        identifier = ParseObjectIdentifier()
        submodel_id_with_shell = self._submodel_id_group_by_shell(aas_shells)
        is_submodel = lambda e: (
            XmlTags.is_match(e.getparent().tag, XmlTags.SUBMODEL)
            and XmlTags.is_match(e.tag, [XmlTags.ID_SHORT, XmlTags.ID])
        )

        for tag, submodel in self._find_elements_by_condition(
            aas_submodels, is_submodel
        ):
            submodel: etree._Element
            if XmlTags.is_match(tag, XmlTags.ID_SHORT):
                identifier.id_short = submodel.text
            elif XmlTags.is_match(tag, XmlTags.ID):
                identifier.id = submodel.text
                key = next(
                    (
                        key
                        for key, value in submodel_id_with_shell.items()
                        if submodel.text in value
                    ),
                    None,
                )
                if key not in self._submodel_identifiers:
                    self._submodel_identifiers[key] = []
                self._submodel_identifiers[key].append(copy.deepcopy(identifier))
                identifier.__init__()

        # submodels
        index_key = 0

        for submodel, level in self._iterate_elements(aas_submodels, 0):
            data_object = self._element_to_object(submodel, level, index_key)
            if data_object is None:
                continue
            submodel_elements.append(data_object)
            index_key += 1

        # concept descriptions
        concept_descriptions = document.find(
            _AAS_KEY + XmlTags.CONCEPT_DESCRIPTIONS.value
        )

        for i, (cd, level) in enumerate(
            self._iterate_elements(concept_descriptions, 0)
        ):
            desc_object = self._element_to_object(cd, level, i)
            if desc_object is None:
                continue
            concept_description_elements.append(desc_object)

        self._objects = list(submodel_elements)
        self._definitions = list(concept_description_elements)

    def parse_xml(self) -> Optional[etree._Element]:
        parser = etree.XMLParser(
            remove_blank_text=True,
            remove_comments=True,
        )
        try:
            root = etree.parse(self.bin, parser).getroot()
        except etree.XMLSyntaxError as e:
            logger.error("xml syntax error: ", e)
            return None
        return root

    def _submodel_id_group_by_shell(
        self,
        aas_shells: etree._Element,
    ) -> Dict[str, List[str]]:
        identifiers: Dict[str, List[str]] = {}

        aas: str = None

        for element in aas_shells.iter():
            element: etree._Element
            if XmlTags.is_match(element.tag, XmlTags.ID_SHORT):
                if aas is None:
                    aas = element.text
                    identifiers[aas] = []
                if aas != element.text:
                    aas = element.text
                    identifiers[aas] = []

            if element is None:
                continue

            prev_element: etree._Element = element.getprevious()
            if prev_element is None:
                continue

            if XmlTags.is_match(prev_element.tag, XmlTags.TYPE) and XmlTags.is_match(
                element.tag, XmlTags.VALUE
            ):
                identifiers[aas].append(element.text)

        return identifiers

    def _element_to_object(
        self, element: etree._Element, level: int, index: int
    ) -> XmlDataObject:
        if element is None:
            return None
        return XmlDataObject(
            element=element,
            level=level,
            index=index,
        )

    def _iterate_elements(
        self, element: etree._Element, level: int = 0
    ) -> Iterable[tuple[etree._Element, int]]:
        if element is None:
            return
        for child in element.iterchildren():
            yield child, level + 1
            yield from self._iterate_elements(child, level + 1)

    def _iterate_children(self, element: etree._Element) -> Iterable[etree._Element]:
        if element is None:
            return
        for child in element:
            yield child

    def _find_elements_by_condition(
        self, element: etree._Element, condition: Callable[[Any], bool]
    ) -> Iterable[List[Tuple[str, etree._Element]]]:
        if element is None:
            return
        for child, _ in self._iterate_elements(element, 0):
            if child is None:
                continue
            if condition(child):
                yield child.tag, child
