from io import BytesIO
import logging
import os
import re
from typing import IO, Iterable, Optional, Union

import pyecma376_2
from aasist.src.guidance.schema_types import AasFileFormat
from aasist.src.guidance.submodel_table_parser import SubmodelTableParser
from aasist.src.guidance.xml.xml_table_parser import XmlTableParser

logger = logging.getLogger(__name__)


class AasxFileReader:

    AASX_ORIGIN_KEY = "http://admin-shell.io/aasx/relationships/aasx-origin"
    AAS_SPEC_KEY = "http://admin-shell.io/aasx/relationships/aas-spec"
    AAS_SPEC_SPLIT_KEY = "http://admin-shell.io/aasx/relationships/aas-spec-split"
    AAS_SUPL_KEY = "http://admin-shell.io/aasx/relationships/aas-suppl"

    def __init__(self, file: Union[os.PathLike, str, IO]):
        self._file = file
        self.zip_reader = pyecma376_2.ZipPackageReader(self._file)

    def load_submodel_table_parsers(
        self,
    ) -> Optional[Iterable[SubmodelTableParser]]:
        parsers = []
        rel = self.zip_reader.get_related_parts_by_type()
        aasx_origin = rel[self.AASX_ORIGIN_KEY]

        if not aasx_origin:
            raise ValueError(f"no aasx origin found in {self._file}")

        aas = aasx_origin[0]
        aas_specs = self.zip_reader.get_related_parts_by_type(aas)[self.AAS_SPEC_KEY]

        if not aas_specs:
            raise ValueError(f"no aas spec found in {aas}")

        aas_specs = set(aas_specs)
        for aas_part in aas_specs:
            parsers.append(self._parse_aas_part(aas_part))
            for split_part in self.zip_reader.get_related_parts_by_type(aas_part)[
                self.AAS_SPEC_SPLIT_KEY
            ]:
                if not split_part:
                    continue
                parsers.append(self._parse_aas_part(split_part))

        return set(parsers)

    def _parse_aas_part(
        self,
        aas_part_name: str,
    ) -> SubmodelTableParser:
        content_type: str = self.zip_reader.get_content_type(aas_part_name)
        extension = re.sub(r".*\.", "", aas_part_name)

        if not content_type.startswith(("application/", "text/")):
            logger.debug(f"not support for this content type: {content_type}")
            return

        if extension == AasFileFormat.XML.value:
            return self._load_xml_parser(aas_part_name)
        if extension == AasFileFormat.JSON.value:
            return self._load_json_parser(aas_part_name)

    def _load_xml_parser(
        self,
        part_name: str,
    ) -> Optional[SubmodelTableParser]:
        try:
            with self.zip_reader.open_part(part_name) as part:
                memory = BytesIO(part.read())
                memory.seek(0)
                xml_parser = XmlTableParser(file=memory)
                return xml_parser
        except Exception as e:
            logger.error(f"failed to read xml format: {part_name} | {e}")
            return

    def _load_json_parser(
        self,
        part_name: str,
    ) -> Optional[SubmodelTableParser]:
        try:
            with self.zip_reader.open_part(part_name) as part:
                # TODO
                pass
        except Exception as e:
            logger.error(f"failed to read json format: {part_name} | {e}")
            return
