from typing import IO

from aasist.src.module.guidance.submodel_table_parser import (
    ParseObject,
    SubmodelTableParser,
)


class JsonObject(ParseObject):
    def __init__(
        self,
    ):
        # TODO
        pass

    def __repr__(self):
        # TODO
        pass


class JsonTableParser(SubmodelTableParser):
    def __init__(self, file: IO):
        super().__init__(file=file)

    # TODO
