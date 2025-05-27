import logging
from typing import IO, Any, Iterable, List, Optional
from lxml import etree
from guidance.submodel_table_parser import ParseObject, SubmodelTableParser
from guidance.xml.xml_schema_types import _AAS_KEY, XmlTags

logger = logging.getLogger(__name__)


class XmlObject(ParseObject):
    def __init__(self, element: etree._Element, level: int = 0):
        super().__init__(
            level=level,
            children=list(element),
        )
        self.element = element
        self.tag = element.tag
        self.text = element.text
        self.parent: Optional[etree._Element] = element.getparent()

    def __repr__(self):
        return f"""{"-" * self.level}> XmlObject(level={self.level}, tag={self.tag}, text={self.text}, parent={self.parent.tag})"""


class XmlTableParser(SubmodelTableParser):

    def __init__(self, file: IO):
        super().__init__(file=file)
        self.bin: IO = file
        self._objects: List[XmlObject] = []
        self._root_submodels: List[str] = []

    def parse_submodels(self, **kwargs: Any):
        self._objects = []
        self._root_submodels = []

        document = self.parse_xml()

        if document is None:
            logger.error("failed to parse xml")
            return None

        elements: List[XmlObject] = []

        aas_submodels = document.find(_AAS_KEY + XmlTags.SUBMODELS.value)

        for submodel, level in self._iterate_elements(aas_submodels, 0):
            xml_object = self._element_to_object(submodel, level)
            if xml_object is None:
                continue
            elements.append(xml_object)
            if XmlTags.is_match(
                xml_object.parent.tag, XmlTags.SUBMODEL
            ) and XmlTags.is_match(xml_object.tag, XmlTags.ID_SHORT):
                self._root_submodels.append(xml_object.text)

        self._objects = list(elements)

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

    def _element_to_object(self, element: etree._Element, level: int) -> XmlObject:
        if element is None:
            return None
        return XmlObject(
            element=element,
            level=level,
        )

    def _iterate_elements(
        self, element: etree._Element, level: int = 0
    ) -> Iterable[tuple[etree._Element, int]]:
        for child in element.iterchildren():
            yield child, level + 1
            yield from self._iterate_elements(child, level + 1)
