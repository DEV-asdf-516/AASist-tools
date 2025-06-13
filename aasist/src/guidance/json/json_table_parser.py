from typing import IO, List

from aasist.src.guidance.submodel_table_parser import ParseObject, SubmodelTableParser


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
        self.bin: IO = file
        self._objects: List[JsonObject] = []
        self._root_submodels: List[str] = []

    # TODO
