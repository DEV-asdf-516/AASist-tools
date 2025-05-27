import copy
from dataclasses import asdict
from types import SimpleNamespace
from typing import Dict, Iterable, List, Tuple

import pandas as pd

from guidance.schema_types import ParentElement
from guidance.submodel_table_extractor import (
    PipelineStage,
    SubmodelTableExtractor,
)

from guidance.xml.xml_table_parser import _AAS_KEY, XmlObject, XmlTableParser, XmlTags
from guidance.submodel_table_model import RowModel


class XmlTableExtractor(SubmodelTableExtractor):

    def __init__(
        self,
        file_name: str,
        parser: XmlTableParser,
        columns: List[str] = None,
        **kwargs,
    ):
        super().__init__(parser=parser, columns=columns)
        self._file_name = file_name
        self._xml_object_store: Dict[str : Iterable[XmlObject]] = {}
        self._submodel_store: Dict[str : Iterable[RowModel]] = {}

    def extract_table(self):
        for parent, children in self._match_submodel_elements(
            submodels=self._parser._objects
        ):
            self._xml_object_store[parent.text] = children

        fsm = XmlRowBuilder()
        rows: List[RowModel] = []

        for key, submodel in self._xml_object_store.items():
            rows = []
            fsm.__init__()

            for i, submodel_element in enumerate(submodel):
                submodel_element: XmlObject
                fsm.handle(submodel_element, idx=i)
                if fsm.is_commited(submodel_element):
                    rows.append(fsm.committed_row)

            if not fsm.current_row.is_empty:
                rows.append(fsm.current_row)

            self._submodel_store[key] = list(rows)

    def _to_dataframes(self) -> Iterable[Tuple[str, pd.DataFrame]]:
        for key, submodel in self._submodel_store.items():
            submodel: Iterable[RowModel]
            to_dicts = [asdict(s) for s in submodel]

            for d in to_dicts:
                d["_definition"] = (
                    "\n".join(
                        str(text) for text in d.get("_definition", []) if d is not None
                    )
                    if isinstance(d.get("_definition"), list)
                    else ""
                )

            df = pd.DataFrame(to_dicts)
            if self.columns:
                df.reindex(columns=self.columns, fill_value="")

            df = df.dropna(how="all")
            df = self._apply_hierarchy(df)
            # TODO: (GUI option) model type 약어 적용
            # kwargs.get('simple_model_type',True)

            yield (key, df)

    def _apply_hierarchy(self, df: pd.DataFrame) -> pd.DataFrame:

        df["depth"] = pd.Categorical(
            df["depth"], categories=sorted(df["depth"].unique()), ordered=True
        ).codes

        df_ = df.apply(lambda row: SimpleNamespace(**row), axis=1)

        depth = df["depth"].unique()

        max_depth = len(depth)
        min_depth = min(dp for dp in depth)

        for i in range(1, max_depth):
            df[f"SMC{i:02}"] = None

        for i, r in enumerate(df_):
            if r is None:
                continue

            if ParentElement.contains(r.model_type):
                df.at[i, f"SMC{r.depth+1:02}"] = r.id_short
                continue

            if r.depth == min_depth:
                df.at[i, f"SMC{r.depth+1:02}"] = "-"
                continue

            if i > 0 and r.depth > min_depth + 1:
                ancestor_idx = self._find_nearest_ancestor(i, df_)
                if ancestor_idx and ancestor_idx > 0:
                    df.at[i, f"SMC{r.depth:02}"] = df_[ancestor_idx].id_short

        group_columns = [f"SMC{i:02}" for i in range(1, max_depth)]
        other_columns = [col for col in df.columns if col not in group_columns]
        other_columns = other_columns[:-1] if not group_columns else other_columns

        df = df[group_columns + other_columns]
        df = df.copy()
        df.drop(["depth", "index"], axis=1, inplace=True)

        return df

    def _find_nearest_ancestor(self, start: int, df_: pd.DataFrame) -> int:
        current_depth = df_[start].depth
        for i in range(start, 0, -1):
            if current_depth > df_[i].depth:
                return i

    def _match_submodel_elements(self, submodels: List[XmlObject]):
        submodel_level = next(
            submodel.level
            for submodel in submodels
            if submodel.text in self._parser._root_submodels
        )
        children: List[XmlObject] = []
        parent = None
        for submodel in submodels:
            if (
                submodel.level == submodel_level
                and submodel.text in self._parser._root_submodels
            ):
                if parent is None:
                    parent = submodel
                if submodel.text != parent.text:
                    yield (parent, children)
                    children = []
                    parent = submodel
                continue
            children.append(submodel)
        if parent is not None:
            yield (parent, children)


ContinueOrBreak = bool


class XmlRowBuilder:
    def __init__(self):
        self.current_row: RowModel = RowModel()
        self.committed_row: RowModel = RowModel()
        self._stage = PipelineStage.idle

    def handle(self, element: XmlObject, idx: int = None):
        """
        idle -> (set_*) -> flush -> idle
        """
        while True:
            match self._stage:
                case PipelineStage.idle:  # default state
                    if self._handle_idle(element):
                        continue
                    return
                case PipelineStage.set_semantic_id:
                    self._handle_set_semantic_id(element)
                    return
                case PipelineStage.set_definition:
                    self._handle_set_definition(element)
                    return
                case PipelineStage.set_model_value:
                    self._handle_set_model_value(element)
                    return
                case PipelineStage.set_id_short:
                    self._handle_set_id_short(element, idx)
                    return
                case PipelineStage.flush:
                    self._handle_flush()
                    continue
                case _:
                    return

    def is_commited(self, element: XmlObject) -> bool:
        if not self.committed_row.is_empty:
            if XmlTags.is_match(element.tag, XmlTags.ID_SHORT):
                return True
        return False

    def _handle_idle(self, element: XmlObject) -> ContinueOrBreak:
        continue_: bool = True
        break_: bool = False

        if XmlTags.is_match(element.tag, XmlTags.ID_SHORT):
            if not self.current_row.is_empty:
                self._stage = PipelineStage.flush
                return continue_

            self._stage = PipelineStage.set_id_short
            return continue_

        if self.current_row.is_empty:
            return break_

        if XmlTags.is_match(element.tag, XmlTags.LANG_STRING_TEXT_TYPE):
            if element.children:
                self._stage = PipelineStage.set_definition
            return break_

        if element.parent.tag == _AAS_KEY + self.current_row.model_type:
            if XmlTags.is_match(element.tag, XmlTags.SEMANTIC_ID):
                self._stage = PipelineStage.set_semantic_id
                return break_
            self._stage = PipelineStage.set_model_value
            return continue_

        return break_

    def _handle_set_semantic_id(self, element: XmlObject):
        if XmlTags.is_match(element.tag, XmlTags.VALUE):
            self.current_row.semantic_id = element.text
            self._stage = PipelineStage.idle

    def _handle_set_definition(self, element: XmlObject):
        if XmlTags.is_match(element.tag, XmlTags.TEXT):
            self.current_row.definition = element.text
            self._stage = PipelineStage.idle

    def _handle_set_model_value(self, element: XmlObject):
        if XmlTags.is_match(element.tag, XmlTags.VALUE_TYPE):
            self.current_row.value_type = element.text
        if XmlTags.is_match(element.tag, XmlTags.VALUE):
            self.current_row.value = element.text
        self._stage = PipelineStage.idle

    def _handle_set_id_short(self, element: XmlObject, idx: int):
        self.current_row.index = idx
        self.current_row.depth = element.level
        self.current_row.id_short = element.text
        self.current_row.model_type = element.parent.tag.replace(_AAS_KEY, "")
        self._stage = PipelineStage.idle

    def _handle_flush(self):
        self.committed_row = copy.deepcopy(self.current_row)
        self.current_row = RowModel()
        self._stage = PipelineStage.idle
