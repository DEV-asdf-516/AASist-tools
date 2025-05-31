import copy
from types import SimpleNamespace
from typing import Dict, Iterable, List, Tuple

import pandas as pd

from guidance.schema_types import SIMPLE_MODEL_TYPES, ParentElement
from guidance.submodel_table_extractor import (
    PipelineStage,
    SubmodelTableExtractor,
)

from guidance.xml.xml_table_parser import (
    _AAS_KEY,
    XmlDataObject,
    XmlTableParser,
    XmlTags,
)
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
        self._xml_object_store: Dict[str : Iterable[XmlDataObject]] = {}
        self._submodel_store: Dict[str : Iterable[RowModel]] = {}
        self._header = {
            "id_short": "idShort",
            "semantic_id": "SemanticID",
            "description": "설명",
            "value": "Value",
            "value_type": "ValueType",
            "model_type": "",
            "reference_type": "참조유형",
            "definition": "정의",
        }

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
                submodel_element: XmlDataObject
                fsm.handle(submodel_element, idx=i)
                if fsm.is_commited(submodel_element):
                    rows.append(fsm.committed_row)

            if not fsm.current_row.is_empty:
                rows.append(fsm.current_row)

            self._submodel_store[key] = list(rows)

    def _to_dataframes(self, **kwargs) -> Iterable[Tuple[str, pd.DataFrame]]:
        for key, submodel in self._submodel_store.items():
            submodel: Iterable[RowModel]
            to_dicts = [s.to_dict() for s in submodel]
            for d in to_dicts:
                d["description"] = (
                    "\n".join(
                        str(text) for text in d.get("description", []) if d is not None
                    )
                    if isinstance(d.get("description"), list)
                    else ""
                )
                if kwargs.get("use_simple_model_type", True):
                    simple_names = {k.lower(): v for k, v in SIMPLE_MODEL_TYPES.items()}
                    d["model_type"] = simple_names.get(
                        d["model_type"].lower(), d["model_type"]
                    )

            df = pd.DataFrame(to_dicts)
            df = df.dropna(how="all")
            df = self._apply_hierarchy(df, **kwargs)

            yield (key, df)

    def _apply_hierarchy(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        hidden_SMC_attributes = kwargs.get("hide_depth_attributes", False)
        df["depth"] = pd.Categorical(
            df["depth"], categories=sorted(df["depth"].unique()), ordered=True
        ).codes

        df_ = df.apply(lambda row: SimpleNamespace(**row), axis=1)

        depth = df["depth"].unique()

        max_depth = len(depth)
        min_depth = min(dp for dp in depth)

        for i in range(1, max_depth):
            df[f"SMC{i:02}"] = None

        prev_ancestors = None

        for i, r in enumerate(df_):
            if r is None:
                continue

            r.index = i

            if hidden_SMC_attributes:
                if not self._have_children(r.index, df_):

                    all_ancestors = list(self._find_all_ancestors(r.index, df_))

                    if not all_ancestors or (
                        self._find_parent(r.index, df_) < 0 and r.depth == min_depth
                    ):
                        df.at[r.index, f"SMC{r.depth+1:02}"] = "-"
                        continue

                    seen = set()
                    current_ancestors = {
                        d: a.id_short
                        for d, a in all_ancestors
                        if (d not in seen and not seen.add(d))
                    }

                    if not prev_ancestors:
                        prev_ancestors = current_ancestors.copy()

                    if (
                        ParentElement.contains(df_[r.index - 1].model_type)
                        or r.index == 0
                        or prev_ancestors != current_ancestors
                    ):
                        for depth, ancestor in current_ancestors.items():
                            df.at[r.index, f"SMC{depth+1:02}"] = ancestor

                    prev_ancestors = current_ancestors.copy()

                elif ParentElement.contains(r.model_type):
                    df.loc[r.index] = None
                    df.at[r.index, f"SMC{r.depth+1:02}"] = r.id_short

                continue

            if ParentElement.contains(r.model_type):
                df.at[r.index, f"SMC{r.depth+1:02}"] = r.id_short
            elif r.depth == min_depth:
                df.at[r.index, f"SMC{r.depth+1:02}"] = "-"
            else:
                parent_idx = self._find_parent(r.index, df_)
                if parent_idx >= 0:
                    df.at[r.index, f"SMC{r.depth:02}"] = df_[parent_idx].id_short

        group_columns = [col for col in df.columns if col.startswith("SMC")]
        other_columns = [col for col in df.columns if col not in group_columns]

        df = df[group_columns + (other_columns if not self.columns else self.columns)]
        df = df.copy()
        if hidden_SMC_attributes:
            df = df[~df["id_short"].isna()]
        df.drop(["depth", "index"], axis=1, inplace=True, errors="ignore")
        df.rename(columns=self._header, inplace=True)
        return df

    def _have_children(self, start: int, df_: pd.DataFrame) -> bool:
        current_depth = df_[start].depth
        for i in range(start + 1, len(df_)):
            if current_depth < df_[i].depth:
                return True
            else:
                return False
        return False

    def _find_all_ancestors(
        self, start: int, df_: pd.DataFrame, min_depth: int = 0
    ) -> Iterable[Tuple[int, SimpleNamespace]]:
        if start <= 0:
            return
        current_depth = df_[start].depth
        for i in range(start - 1, -1, -1):
            if current_depth > df_[i].depth and ParentElement.contains(
                df_[i].model_type
            ):
                yield (df_[i].depth, df_[i])
            if df_[i].depth == min_depth:
                return

    def _find_parent(self, start: int, df_: pd.DataFrame) -> int:
        if start <= 0:
            return -1
        current_depth = df_[start].depth
        for i in range(start - 1, -1, -1):
            if current_depth > df_[i].depth and ParentElement.contains(
                df_[i].model_type
            ):
                return i
        return -1

    def _match_submodel_elements(self, submodels: List[XmlDataObject]):
        submodel_level = next(
            submodel.level
            for submodel in submodels
            if submodel.text in self._parser._root_submodels
        )
        children: List[XmlDataObject] = []
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

    def handle(self, element: XmlDataObject, idx: int = None):
        """
        idle -> (set_*) -> flush -> idle
        """
        while True:
            """
            continue: process next step
            return: end of current step processing
            """
            match self._stage:
                case PipelineStage.idle:  # default state
                    if self._handle_idle(element):
                        continue
                    return
                case PipelineStage.set_semantic_id:
                    self._handle_set_semantic_id(element)
                    return
                case PipelineStage.set_description:
                    self._handle_set_description(element)
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

    def is_commited(self, element: XmlDataObject) -> bool:
        if not self.committed_row.is_empty:
            if XmlTags.is_match(element.tag, XmlTags.ID_SHORT):
                return True
        return False

    def _handle_idle(self, element: XmlDataObject) -> ContinueOrBreak:
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

        if (
            XmlTags.is_match(element.tag, XmlTags.LANG_STRING_TEXT_TYPE)
            and self.current_row.model_type
        ):
            # TODO MLP 검사
            if element.children:
                self._stage = PipelineStage.set_description
            return break_

        if element.parent.tag == _AAS_KEY + self.current_row.model_type:
            if XmlTags.is_match(element.tag, XmlTags.SEMANTIC_ID):
                self._stage = PipelineStage.set_semantic_id
                return break_
            self._stage = PipelineStage.set_model_value
            return continue_

        return break_

    def _handle_set_semantic_id(self, element: XmlDataObject):
        if XmlTags.is_match(element.tag, XmlTags.TYPE) and XmlTags.is_match(
            element.parent.tag, XmlTags.KEY
        ):
            self.current_row.reference_type = element.text
        if XmlTags.is_match(element.tag, XmlTags.VALUE):
            self.current_row.semantic_id = element.text
            self._stage = PipelineStage.idle

    def _handle_set_description(self, element: XmlDataObject):
        if XmlTags.is_match(element.tag, XmlTags.TEXT):
            self.current_row.description = element.text
            self._stage = PipelineStage.idle

    def _handle_set_model_value(self, element: XmlDataObject):
        if XmlTags.is_match(element.tag, XmlTags.VALUE_TYPE):
            self.current_row.value_type = element.text
        if XmlTags.is_match(element.tag, XmlTags.VALUE):
            self.current_row.value = element.text
        self._stage = PipelineStage.idle

    def _handle_set_id_short(self, element: XmlDataObject, idx: int):
        self.current_row.index = idx
        self.current_row.depth = element.level
        self.current_row.id_short = element.text
        self.current_row.model_type = element.parent.tag.replace(_AAS_KEY, "")
        self._stage = PipelineStage.idle

    def _handle_flush(self):
        self.committed_row = copy.deepcopy(self.current_row)
        self.current_row = RowModel()
        self._stage = PipelineStage.idle
