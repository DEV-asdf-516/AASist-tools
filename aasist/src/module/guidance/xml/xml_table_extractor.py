import logging
import traceback
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Tuple

import pandas as pd

from aasist.src.gui.handler import _GUIDANCE_LOG_NAME, LogLevel, QueueHandler
from aasist.src.module.guidance.schema_types import (
    SIMPLE_MODEL_TYPES,
    ParentElement,
    TableFormat,
)
from aasist.src.module.guidance.submodel_table_extractor import (
    DefaultSubmodel,
    SubmodelTableExtractor,
)

from aasist.src.module.guidance.submodel_table_parser import ParseObjectIdentifier
from aasist.src.module.guidance.xml.xml_object_builder import (
    XmlConceptDescriptionBuilder,
    XmlRowBuilder,
)
from aasist.src.module.guidance.xml.xml_schema_types import XmlTags
from aasist.src.module.guidance.xml.xml_table_parser import (
    XmlDataObject,
    XmlTableParser,
)
from aasist.src.module.guidance.submodel_table_model import (
    ConceptDescriptionModel,
    RowModel,
)

logger = logging.getLogger(__name__)


class XmlTableExtractor(SubmodelTableExtractor):

    def __init__(
        self,
        file_name: str,
        parser: XmlTableParser,
        submodels: List[str] = None,
        columns: List[str] = None,
        **kwargs,
    ):
        super().__init__(
            parser=parser,
            submodels=submodels,
            columns=columns,
            log_handler=QueueHandler(_GUIDANCE_LOG_NAME),
        )
        self._file_name = file_name
        self._xml_object_store: Dict[str : Tuple[str, Iterable[XmlDataObject]]] = {}
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
        self._cd_store: List[ConceptDescriptionModel] = []
        self.log_handler = QueueHandler(_GUIDANCE_LOG_NAME)
        self.use_simple_model_type: bool = kwargs.get("use_simple_model_type")
        self.hide_depth_attributes: bool = kwargs.get("hide_depth_attributes")

    def extract_table(self):
        self._assemble_concept_descriptions(
            concept_descriptions=self._parser._definitions
        )

        for parent, children, shell in self._match_submodel_elements(
            submodels=self._parser._objects
        ):
            submodel_name: str = parent.lower()
            is_sub_matched = any(
                submodel_name in sub.replace("_", "") for sub in self.submodels
            )
            all_submodels = "all_submodels" in self.submodels
            etc_submodels = "etc" in self.submodels
            if any(
                [
                    is_sub_matched,
                    all_submodels,
                    not self.submodels,  # 아무것도 선택하지 않았다면 전부 추출
                    not is_sub_matched
                    and etc_submodels
                    and not DefaultSubmodel.is_default(parent),
                ]
            ):
                if shell is None:
                    continue
                key = f"{shell}_{parent}"
                self._xml_object_store[key] = children
                self.log_handler.add(f"Start extracting Submodel: {key}")

        row_builder = XmlRowBuilder()
        rows: List[RowModel] = []

        for key, submodel in self._xml_object_store.items():
            rows = []
            row_builder.__init__()

            for i, submodel_element in enumerate(submodel):
                submodel_element: XmlDataObject
                row_builder.handle(submodel_element, idx=i)
                if row_builder.is_committed(submodel_element):
                    cd: ConceptDescriptionModel = self._find_concept_description(
                        row_builder.committed_instance.id_short,
                        row_builder.committed_instance.semantic_id,
                    )
                    row_builder.committed_instance.definition = (
                        cd.definition if cd else None
                    )
                    rows.append(row_builder.committed_instance)

            if not row_builder.current_instance.is_empty:
                rows.append(row_builder.current_instance)

            self._submodel_store[key] = list(rows)

    def _to_dataframes(self) -> Iterable[Tuple[str, pd.DataFrame]]:
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
                d["definition"] = (
                    "\n".join(
                        str(text) for text in d.get("definition", []) if d is not None
                    )
                    if isinstance(d.get("definition"), list)
                    else ""
                )
                if self.use_simple_model_type:
                    simple_names = {k.lower(): v for k, v in SIMPLE_MODEL_TYPES.items()}
                    d["model_type"] = simple_names.get(
                        d["model_type"].lower(), d["model_type"]
                    )

            df = pd.DataFrame(to_dicts)
            df = df.dropna(how="all")
            result_df = self._apply_hierarchy(df)
            result_df.rename(columns=self._header, inplace=True)
            result_df.rename(
                columns={
                    col: f"SMC{int(col[3:])-1:02d}"
                    for col in df.columns
                    if col.startswith("SMC")
                },
                inplace=True,
            )
            result_df = result_df.iloc[1:, 1:]

            yield (key, result_df)

    def export(self, format: TableFormat):
        self.log_handler.add(f"Convert Submodel metadata to {format.name} ...")
        try:
            super().export(format, log_handler=self.log_handler)
            total_count = len(self._submodel_store)
            self.log_handler.add(
                f"{self.success_count} of {total_count} Submodels from {self._file_name} exported successfully.",
                log_level=LogLevel.SUCCESS,
            )
            self.log_handler.add(
                f"{self.failure_count} of {total_count} failed.",
                log_level=LogLevel.ERROR if self.failure_count > 0 else LogLevel.TRACE,
            )
        except Exception as e:
            traceback.print_exc()
            self.log_handler.add(
                f"An error occurred while exporting the file ...",
                log_level=LogLevel.ERROR,
            )

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

        prev_ancestors: dict[int, Any] = None

        for i, r in enumerate(df_):
            if r is None:
                continue

            r.index = i

            if self.hide_depth_attributes:
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
        if self.hide_depth_attributes:
            df = df[~df["id_short"].isna()]
        df.drop(["depth", "index"], axis=1, inplace=True, errors="ignore")
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
        try:
            identifier_map: Dict[str, Tuple[str, ParseObjectIdentifier]] = {
                identifier.id: (key, identifier)
                for key, identifiers in self._parser._submodel_identifiers.items()
                for identifier in identifiers
            }

            submodel_level = min(submodel.level for submodel in submodels)

            children: List[XmlDataObject] = []

            current_submodel: Tuple[str, ParseObjectIdentifier] = None
            for submodel in submodels:

                if submodel.level == submodel_level:
                    if not current_submodel:  # 첫 서브모델
                        continue

                    aas_shell, identifier = current_submodel

                    yield (identifier.id_short, children, aas_shell)

                    children = []

                    continue

                if XmlTags.is_match(submodel.tag, XmlTags.ID):
                    identifier: ParseObjectIdentifier

                    current_submodel = identifier_map.get(submodel.text)
                    aas_shell, identifier = current_submodel

                children.append(submodel)

            if children:
                aas_shell, identifier = current_submodel
                yield (identifier.id_short, children, aas_shell)

        except ValueError as e:
            logger.error(f"Error matching submodel elements: {e}")
            pass

    def _assemble_concept_descriptions(self, concept_descriptions: List[XmlDataObject]):
        self._cd_store = []

        cd_builder: XmlConceptDescriptionBuilder = XmlConceptDescriptionBuilder()
        cds: List[ConceptDescriptionModel] = []

        for cd in concept_descriptions:
            cd_builder.handle(cd)
            if cd_builder.is_committed(cd):
                cds.append(cd_builder.committed_instance)
                continue

            if not cd_builder.current_instance.is_empty:
                cds.append(cd_builder.current_instance)

        self._cd_store = cds.copy()

    def _find_concept_description(
        self,
        id_short: str,
        semantic_id: str,
    ) -> ConceptDescriptionModel | None:
        for i, cd in enumerate(self._cd_store):
            if cd.id_short == id_short and cd.id == semantic_id:
                # TODO: AAS 여러개일때 definition 추출 안되는 이슈 수정
                return self._cd_store.pop(i)
        return None
