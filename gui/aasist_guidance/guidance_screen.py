from typing import Dict, Iterable, List, Tuple
import customtkinter as ctk

from gui.aasist_guidance.options import (
    AttiributeOptions,
    FileFormatToggleButton,
    SettingOptions,
    SubmodelOptions,
)
from gui.common.clear_button import ClearButton
from gui.common.default_button import DefaultButton
from gui.common.divider import Divider
from gui.common.file_exporter import FileExporter
from gui.common.file_selector import FileSelector
from guidance.aasx_file_reader import AasxFileReader
from guidance.json.json_table_parser import JsonTableParser
from guidance.schema_types import TableFormat
from guidance.submodel_table_parser import SubmodelTableParser
from guidance.xml.xml_table_extractor import XmlTableExtractor
from guidance.xml.xml_table_parser import XmlTableParser


class GuidanceScreen(ctk.CTkFrame):
    default_options = {
        "word": True,
        "excel": False,
        "all_submodels": True,
        "identification": True,
        "documentation": True,
        "cad": True,
        "carbon_footprint": True,
        "hierarchical_structures": True,
        "digital_nameplate": True,
        "technical_data": True,
        "operational_data": True,
        "all_attributes": False,
        "model_type": True,
        "id_short": True,
        "semantic_id": True,
        "depth": True,
        "definition": False,
        "description": True,
        "value": False,
        "value_type": False,
        "reference_type": False,
        "simple_model_type": True,
        "depth_ellipses": False,
    }

    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent)
        self.parent = parent
        self._readers: List[Tuple[str, AasxFileReader]] = []
        self._parsers: List[SubmodelTableParser] = []
        self.chosen_options: Dict[str, bool] = self.default_options.copy()
        self.theme_data = ctk.ThemeManager.theme
        self._table_format: TableFormat = TableFormat.DOCX
        self.layout()

    def layout(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        browse_frame = ctk.CTkFrame(
            self, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        browse_frame.grid(row=0, column=0, sticky=ctk.EW)
        browse_frame.grid_columnconfigure(0, weight=1)

        self.file_selector = FileSelector(
            browse_frame,
            on_files_selected=self.handle_file_selected,
            file_types=[("AAS Files", "*.aasx")],
            bg_color=self.theme_data["CTkFrame"]["fg_color"],
        )

        self.file_selector.grid(row=0, column=0, sticky=ctk.EW, pady=(8, 0), padx=8)

        horizontal_divider = Divider(self, orientation="horizontal", thickness=2)
        horizontal_divider.grid_horizontal(row=1, column=0, pady=(4, 4), padx=8)

        content_frame = ctk.CTkFrame(
            self, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        content_frame.grid(row=2, column=0, sticky=ctk.NSEW, pady=(0, 8))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(
            content_frame, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        left_frame.grid(row=0, column=0, sticky=ctk.NSEW, padx=(16, 0))

        right_frame = ctk.CTkFrame(
            content_frame, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        right_frame.grid(row=0, column=1, sticky=ctk.NSEW, padx=(0, 16))

        self.option_panel(left_frame)
        self.output_panel(right_frame)

    # left panel
    def option_panel(self, parent: ctk.CTkFrame):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(
            parent, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        header_frame.grid(row=0, column=0, sticky=ctk.EW)
        header_frame.grid_columnconfigure(0, weight=1)

        # Title section
        title_label = ctk.CTkLabel(
            header_frame,
            text="Submodel Extract options",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=self.theme_data["CTkLabel"]["fg_color"],
        )
        title_label.grid(row=0, column=0, sticky=ctk.W, padx=16)

        default_button = DefaultButton(
            header_frame,
            on_click=self.reset_default_options,
            default_options=self.default_options,
            bg_color=self.theme_data["CTkFrame"]["fg_color"],
        )
        default_button.grid(row=0, column=2, sticky=ctk.E)

        options_container = ctk.CTkFrame(
            parent, fg_color="#ededed", border_width=1, corner_radius=6
        )
        options_container.grid(
            row=1, column=0, columnspan=3, sticky=ctk.NSEW, padx=(0, 8), pady=(0, 8)
        )
        options_container.grid_columnconfigure(0, weight=1)

        # File format section
        format_label = ctk.CTkLabel(
            options_container,
            text="파일 확장자",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        format_label.grid(row=0, column=0, sticky=ctk.W, pady=(8, 0), padx=16)

        self.toggle_button = FileFormatToggleButton(
            options_container, on_toggle=self.handle_toggle_changed
        )
        self.toggle_button.grid(row=1, column=0, sticky=ctk.W, pady=8, padx=16)

        file_format_divider = Divider(
            options_container, orientation="horizontal", thickness=2
        )
        file_format_divider.grid_horizontal(row=2, column=0, sticky=ctk.EW)

        # Submodels section
        submodel_label = ctk.CTkLabel(
            options_container,
            text="Submodels",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        submodel_label.grid(row=3, column=0, sticky=ctk.W, pady=4, padx=16)

        self.submodel_options = SubmodelOptions(
            options_container,
            on_check=self.handle_checkbox_options_changed,
            chosen_options=self.chosen_options,
            bg_color="#ededed",
        )

        self.submodel_options.grid(row=4, column=0, sticky=ctk.EW, pady=8, padx=16)

        sumbodel_divider = Divider(
            options_container, orientation="horizontal", thickness=2
        )
        sumbodel_divider.grid_horizontal(row=5, column=0, sticky=ctk.EW)

        # Attributes section
        attribute_label = ctk.CTkLabel(
            options_container,
            text="Attributes",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        attribute_label.grid(row=6, column=0, sticky=ctk.W, pady=4, padx=16)
        attribute_sub_label = ctk.CTkLabel(
            options_container,
            text="Guidanace for Submodel Data",
            font=ctk.CTkFont(size=14),
            text_color="#9C9C9C",
        )
        attribute_sub_label.grid(row=7, column=0, sticky=ctk.W, pady=(0, 4), padx=16)

        self.attribute_options = AttiributeOptions(
            options_container,
            on_check=self.handle_checkbox_options_changed,
            chosen_options=self.chosen_options,
            default_options=self.default_options,
            bg_color="#ededed",
        )
        self.attribute_options.grid(row=8, column=0, sticky=ctk.EW, pady=8, padx=16)

        attribute_divider = Divider(
            options_container, orientation="horizontal", thickness=2
        )
        attribute_divider.grid_horizontal(row=9, column=0, sticky=ctk.EW)

        # Setting section
        setting_label = ctk.CTkLabel(
            options_container,
            text="설정",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        setting_label.grid(row=10, column=0, sticky=ctk.W, pady=4, padx=16)

        self.setting_options = SettingOptions(
            options_container,
            on_check=self.handle_checkbox_options_changed,
            chosen_options=self.chosen_options,
            default_options=self.default_options,
            bg_color="#ededed",
        )

        self.setting_options.grid(row=11, column=0, sticky=ctk.EW, pady=8, padx=16)

    # right panel
    def output_panel(self, parent: ctk.CTkFrame):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        header_frame = ctk.CTkFrame(
            parent, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        header_frame.grid(row=0, column=0, sticky=ctk.EW, pady=(16, 8))
        header_frame.grid_columnconfigure(0, weight=1)

        # Title section
        title_label = ctk.CTkLabel(
            header_frame,
            text="Outputs",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=self.theme_data["CTkLabel"]["fg_color"],
        )
        title_label.grid(row=0, column=0, sticky=ctk.W, padx=16)

        # output box section
        # TODO : 로그 출력
        output_box = ctk.CTkTextbox(parent, state=ctk.DISABLED, width=600)
        output_box.grid(row=1, column=0, sticky=ctk.NSEW, padx=8, pady=8)

        # button section
        buttons_frame = ctk.CTkFrame(
            parent, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        buttons_frame.grid(row=1, column=1, sticky=ctk.NE, pady=(0, 8), padx=(4, 0))

        file_exporter = FileExporter(
            buttons_frame,
            on_export=lambda: self.handle_export_created_files(
                columns=[
                    key
                    for key, value in self.chosen_options.items()
                    if key
                    in {k for k in self.attribute_options.copy_chosen_options.keys()}
                    and value == True
                ],
                simple_model_type=self.chosen_options.get("simple_model_type", True),
                depth_ellipses=self.chosen_options.get("depth_ellipses", False),
            ),
        )
        file_exporter.grid(row=0, column=0, sticky=ctk.E, pady=8)

        clear_button = ClearButton(buttons_frame, on_click=self.handle_clear_output)
        clear_button.grid(row=1, column=0, sticky=ctk.E, pady=(0, 8))

    def _from_readers(self) -> Iterable[Tuple[str, List[SubmodelTableParser]]]:
        for file, reader in self._readers:
            parsers = list(reader.load_submodel_table_parsers())
            if not parsers:
                # TODO: handle error
                continue
            yield (file, parsers)

    def handle_file_selected(self, file_paths: List[str]):
        self._readers.clear()
        self.loaded_files = file_paths
        for file in file_paths:
            self._readers.append((file, AasxFileReader(file)))

    def handle_export_created_files(self, **kwargs):
        columns: List[str] = kwargs.get("columns", None)

        if columns:
            columns = [col for col in columns if not col.startswith("all")]

        # TODO: 선택한 서브모델만

        use_simple_model_type = kwargs.get("simple_model_type")
        hide_depth_attributes = kwargs.get("depth_ellipses")

        for file, parsers in self._from_readers():
            for parser in parsers:
                parser.parse_submodels(**kwargs)

                if isinstance(parser, XmlTableParser):
                    table_extractor = XmlTableExtractor(
                        file_name=file, parser=parser, columns=columns
                    )
                    table_extractor.extract_table()
                    table_extractor.export(
                        format=self._table_format,
                        use_simple_model_type=use_simple_model_type,
                        hide_depth_attributes=hide_depth_attributes,
                    )

                if isinstance(parser, JsonTableParser):
                    # TODO
                    pass

    def handle_clear_output(self):
        # TODO
        pass

    def handle_toggle_changed(self, option: str):
        if "word" in option.lower():
            self.chosen_options.update({"word": True, "excel": False})
            self._table_format = TableFormat.DOCX
        elif "excel" in option.lower():
            self.chosen_options.update({"word": False, "excel": True})
            self._table_format = TableFormat.XLSX

    def handle_checkbox_options_changed(self, options: Dict[str, bool]):
        self.chosen_options.update(options)

    def reset_default_options(self, default_options: Dict[str, bool]):
        self.chosen_options = default_options.copy()
        self.toggle_button.init_buttons()
        self.submodel_options.init_checkboxes()
        self.attribute_options.init_checkboxes()
        self.setting_options.init_checkboxes()
