import copy
from guidance.submodel_table_extractor import (
    ConceptDescriptionPipelineStage,
    RowPipelineStage,
)
from guidance.submodel_table_model import ConceptDescriptionModel, RowModel
from guidance.submodel_table_model_builder import ModelBuilder
from guidance.xml.xml_schema_types import _AAS_KEY, XmlTags
from guidance.xml.xml_table_parser import XmlDataObject


ContinueOrBreak = bool


class XmlRowBuilder(ModelBuilder):
    def __init__(self):
        super().__init__(
            current_instance=RowModel(),
            committed_instance=RowModel(),
            stage=RowPipelineStage.idle,
        )
        self.committed_instance: RowModel = self.committed_instance
        self.current_instance: RowModel = self.current_instance

    def handle(self, object: XmlDataObject, **kwargs):
        """
        idle -> (set_*) -> flush -> idle
        """
        idx: int = kwargs.get("idx", None)
        while True:
            """
            continue: process next step
            return: end of current step processing
            """
            match self._stage:
                case RowPipelineStage.idle:  # default state
                    if self._handle_idle(object):
                        continue
                    return
                case RowPipelineStage.set_semantic_id:
                    self._handle_set_semantic_id(object)
                    return
                case RowPipelineStage.set_description:
                    self._handle_set_description(object)
                    return
                case RowPipelineStage.set_MLP_model_value:
                    self._handle_set_MLP_model_value(object)
                    return
                case RowPipelineStage.set_model_value:
                    self._handle_set_model_value(object)
                    return
                case RowPipelineStage.set_id_short:
                    self._handle_set_id_short(object, idx)
                    return
                case RowPipelineStage.flush:
                    self._handle_flush()
                    continue
                case _:
                    return

    def is_committed(self, object: XmlDataObject) -> bool:
        if not self.committed_instance.is_empty:
            if XmlTags.is_match(object.tag, XmlTags.ID_SHORT):
                return True
        return False

    def _handle_idle(self, object: XmlDataObject) -> ContinueOrBreak:
        continue_: bool = True
        break_: bool = False

        if XmlTags.is_match(object.tag, XmlTags.ID_SHORT):
            if not self.current_instance.is_empty:
                self._stage = RowPipelineStage.flush
                return continue_
            self._stage = RowPipelineStage.set_id_short
            return continue_

        if self.current_instance.is_empty:
            return break_

        if (
            XmlTags.is_match(object.tag, XmlTags.LANG_STRING_TEXT_TYPE)
            and self.current_instance.model_type
        ):
            if (
                self.current_instance.model_type
                == XmlTags.MULTI_LANGUAGE_PROPERTY.value
            ):
                self._stage = RowPipelineStage.set_MLP_model_value
                return break_
            if object.children:
                self._stage = RowPipelineStage.set_description
            return break_

        if object.parent.tag == _AAS_KEY + self.current_instance.model_type:
            if XmlTags.is_match(object.tag, XmlTags.SEMANTIC_ID):
                self._stage = RowPipelineStage.set_semantic_id
                return break_
            self._stage = RowPipelineStage.set_model_value
            return continue_

        return break_

    def _handle_set_semantic_id(self, object: XmlDataObject):
        if XmlTags.is_match(object.tag, XmlTags.TYPE) and XmlTags.is_match(
            object.parent.tag, XmlTags.KEY
        ):
            self.current_instance.reference_type = object.text
        if XmlTags.is_match(object.tag, XmlTags.VALUE):
            self.current_instance.semantic_id = object.text
            self._stage = RowPipelineStage.idle

    def _handle_set_description(self, object: XmlDataObject):
        if XmlTags.is_match(object.tag, XmlTags.TEXT):
            self.current_instance.description = object.text
            self._stage = RowPipelineStage.idle

    def _handle_set_MLP_model_value(self, object: XmlDataObject):
        if XmlTags.is_match(object.tag, XmlTags.TEXT):
            self.current_instance.value = object.text
            self._stage = RowPipelineStage.idle

    def _handle_set_model_value(self, object: XmlDataObject):
        if XmlTags.is_match(object.tag, XmlTags.VALUE_TYPE):
            self.current_instance.value_type = object.text
        if XmlTags.is_match(object.tag, XmlTags.VALUE):
            self.current_instance.value = object.text
        self._stage = RowPipelineStage.idle

    def _handle_set_id_short(self, object: XmlDataObject, idx: int):
        self.current_instance.index = idx
        self.current_instance.depth = object.level
        self.current_instance.id_short = object.text
        self.current_instance.model_type = object.parent.tag.replace(_AAS_KEY, "")
        self._stage = RowPipelineStage.idle

    def _handle_flush(self):
        self.committed_instance = copy.deepcopy(self.current_instance)
        self.current_instance = RowModel()
        self._stage = RowPipelineStage.idle


class XmlConceptDescriptionBuilder(ModelBuilder):
    def __init__(self):
        super().__init__(
            current_instance=ConceptDescriptionModel(),
            committed_instance=ConceptDescriptionModel(),
            stage=ConceptDescriptionPipelineStage.idle,
        )
        self.committed_instance: ConceptDescriptionModel = self.committed_instance
        self.current_instance: ConceptDescriptionModel = self.current_instance

    def handle(self, object: XmlDataObject, **kwargs):
        while True:
            match self._stage:
                case ConceptDescriptionPipelineStage.idle:
                    if self._handle_idle(object):
                        continue
                    return
                case ConceptDescriptionPipelineStage.set_definition:
                    self._handle_set_definition(object)
                    return
                case ConceptDescriptionPipelineStage.flush:
                    self._handle_flush()
                    continue
                case _:
                    return

    def is_committed(self, object: XmlDataObject) -> bool:
        if not self.committed_instance.is_empty:
            if XmlTags.is_match(object.tag, XmlTags.CONCEPT_DESCRIPTION):
                return True
        return False

    def _handle_idle(self, object: XmlDataObject) -> ContinueOrBreak:
        continue_: bool = True
        break_: bool = False

        if XmlTags.is_match(object.tag, XmlTags.CONCEPT_DESCRIPTION):
            if not self.current_instance.is_empty:
                self._stage = ConceptDescriptionPipelineStage.flush
                return continue_
            return break_

        if XmlTags.is_match(object.tag, XmlTags.ID_SHORT):
            self.current_instance.id_short = object.text
            return break_

        if XmlTags.is_match(object.tag, XmlTags.ID):
            self.current_instance.id = object.text
            return break_

        if XmlTags.is_match(object.tag, XmlTags.DEFINITION):
            self._stage = ConceptDescriptionPipelineStage.set_definition
            return break_

        if not self.current_instance.is_empty:
            self._stage = ConceptDescriptionPipelineStage.set_definition
            return continue_

        return break_

    def _handle_set_definition(self, object: XmlDataObject):
        if XmlTags.is_match(object.tag, XmlTags.TEXT) and XmlTags.is_match(
            object.parent.tag, XmlTags.LANG_STRING_DEFINITION_TYPE_IEC_61360
        ):
            self.current_instance.definition = object.text
        self._stage = ConceptDescriptionPipelineStage.idle

    def _handle_flush(self):
        self.committed_instance = copy.deepcopy(self.current_instance)
        self.current_instance = ConceptDescriptionModel()
        self._stage = ConceptDescriptionPipelineStage.idle
