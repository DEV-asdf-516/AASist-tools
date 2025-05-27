from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import (
    Dict,
    Iterable,
    List,
    Tuple,
)

from docx import Document
import pandas as pd
from guidance.schema_types import TableFormat
from guidance.submodel_table_parser import ParseObject, SubmodelTableParser


class PipelineStage(Enum):
    idle = auto()
    set_id_short = auto()
    set_model_value = auto()
    set_semantic_id = auto()
    set_definition = auto()
    flush = auto()


class SubmodelTableExtractor(ABC):
    # TODO (GUI option) 필드 추출 가능
    # TODO (GUI option) 지원확장자 docx, xlsx
    # TODO (GUI option) aas파일이 보유한 Submodel 중에서 선택한 Submodel 추출 가능(default: 모든 Submodel) > extract
    def __init__(
        self, parser: SubmodelTableParser, columns: List[str] = None, **kwargs
    ):
        self._parser = parser
        self._submodel_store: Dict[str, ParseObject] = {}
        self.columns = columns
        self._file_name = kwargs.get("file_name", None)

    def export(self, format: TableFormat):
        prefix = (self._file_name or "output").split(".")[0]

        for submodel, df in self._to_dataframes():
            if format == TableFormat.DOCX:
                docx = Document()
                table = docx.add_table(rows=1, cols=len(df.columns))
                table.style = "Table Grid"
                table.autofit = True

                for i, column in enumerate(df.columns):
                    table.cell(0, i).text = column

                for row in df.itertuples(index=False):
                    cells = table.add_row().cells
                    for i, value in enumerate(row):
                        cells[i].text = (
                            ""
                            if value is None or not isinstance(value, str)
                            else str(value)
                        )
                docx.save(prefix + "_" + submodel + ".docx")

            if format == TableFormat.XLSX:
                df.to_excel(prefix + "_" + submodel + ".xlsx", index=False)

    @abstractmethod
    def extract_table(self):
        pass

    @abstractmethod
    def _to_dataframes(self) -> Iterable[Tuple[str, pd.DataFrame]]:
        pass
