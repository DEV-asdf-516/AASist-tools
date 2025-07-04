from typing import Any, Dict, List, Optional, Tuple
import customtkinter as ctk
import copy
from aasist.src.gui.aasist_test.options import (
    IdtaOptions,
    KosmoOptions,
    TestExecuteButton,
    UrlInputForm,
)
from aasist.src.gui.common.clear_button import ClearButton
from aasist.src.gui.common.default_button import DefaultButton
from aasist.src.gui.common.divider import Divider
from aasist.src.gui.common.file_exporter import FileExporter
from aasist.src.gui.common.file_selector import FileSelector
from aasist.src.gui.common.log_box import LogBox
from aasist.src.gui.common.tree_checkbox_frame import TreeCheckboxFrame
from aasist.src.gui.handler import _TEST_LOG_NAME, QueueHandler
from aasist.src.module.tester.file.file_verificator import TestFileVerficator
from aasist.src.module.tester.constants import IDTA, KOSMO


class TestScreen(ctk.CTkFrame):
    default_options = {
        IDTA.standard.name: True,
        IDTA.optional.name: False,
        IDTA.aasd_002.name: False,
        IDTA.aasd_005.name: False,
        IDTA.aasd_006.name: False,
        IDTA.aasd_007.name: False,
        # IDTA.aasd_012.name: False,
        IDTA.aasd_014.name: False,
        IDTA.aasd_020.name: False,
        # IDTA.aasd_021.name: False,
        # IDTA.aasd_022.name: False,
        # IDTA.aasd_077.name: False,
        IDTA.aasd_090.name: False,
        IDTA.aasd_107.name: False,
        # IDTA.aasd_108.name: False,
        IDTA.aasd_109.name: False,
        IDTA.aasd_114.name: False,
        # IDTA.aasd_115.name: False,
        IDTA.aasd_116.name: False,
        IDTA.aasd_117.name: False,
        IDTA.aasd_118.name: False,
        IDTA.aasd_119.name: False,
        IDTA.aasd_120.name: False,
        IDTA.aasd_121.name: False,
        IDTA.aasd_122.name: False,
        IDTA.aasd_123.name: False,
        IDTA.aasd_124.name: False,
        IDTA.aasd_125.name: False,
        IDTA.aasd_126.name: False,
        IDTA.aasd_127.name: False,
        IDTA.aasd_128.name: False,
        IDTA.aasd_129.name: False,
        IDTA.aasd_130.name: False,
        IDTA.aasd_131.name: False,
        IDTA.aasd_133.name: False,
        IDTA.aasd_134.name: False,
        IDTA.aasc_3a_002.name: False,
        # IDTA.aasc_3a_003.name: False,
        IDTA.aasc_3a_004.name: False,
        IDTA.aasc_3a_005.name: False,
        IDTA.aasc_3a_006.name: False,
        IDTA.aasc_3a_007.name: False,
        IDTA.aasc_3a_008.name: False,
        IDTA.aasc_3a_009.name: False,
        IDTA.aasc_3a_010.name: False,
        # IDTA.aasc_3c_050.name: False,
        KOSMO.aas_thumbnail.name: True,
        KOSMO.aas_id_short.name: True,
        KOSMO.aas_id.name: True,
        KOSMO.aas_submodel.name: True,
        KOSMO.aas_global_asset_id.name: False,
        KOSMO.aas_type.name: True,
        KOSMO.submodel_id_short.name: True,
        KOSMO.submodel_id.name: True,
        KOSMO.submodel_semantic_id.name: True,
        KOSMO.submodel_kind.name: True,
        KOSMO.smc_id_short.name: True,
        KOSMO.smc_cd_mapping.name: False,
        KOSMO.prop_id_short.name: True,
        KOSMO.prop_cd_mapping.name: True,
        KOSMO.prop_value.name: False,
        KOSMO.cd_id_short.name: True,
        KOSMO.cd_id.name: True,
        KOSMO.cd_definition.name: True,
    }

    idta_group = ["idta", "aasd", "aasc_3a"]
    kosmo_group = ["kosmo_aas", "kosmo_submodel", "kosmo_smc", "kosmo_prop", "kosmo_cd"]

    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent)
        self._default_expanded_states = {
            k: k == "idta" for k in self.idta_group + self.kosmo_group
        }
        self._files: List[str] = []
        self._url: str = None
        self.parent = parent
        self.chosen_options: Dict[str, bool] = self.default_options.copy()
        self.expanded_states: Dict[str, bool] = self._default_expanded_states.copy()
        self.theme_data = ctk.ThemeManager.theme
        self.log_handler = QueueHandler(_TEST_LOG_NAME)
        self.layout()

    def layout(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(
            self, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        header_frame.grid(row=0, column=0, sticky=ctk.EW)
        header_frame.grid_columnconfigure(0, weight=1)

        self.file_selector = FileSelector(
            header_frame,
            on_files_selected=self.handle_file_selected,
            file_types=[
                ("AAS Files", "*.aasx"),
                ("XML Files", "*.xml"),
                ("JSON Files", "*.json"),
            ],
            bg_color=self.theme_data["CTkFrame"]["fg_color"],
        )
        self.file_selector.grid(row=0, column=0, sticky=ctk.EW, pady=(8, 0), padx=8)

        file_horizontal_divider = Divider(
            header_frame, orientation="horizontal", thickness=2
        )
        file_horizontal_divider.grid_horizontal(row=1, column=0, pady=(4, 4), padx=8)

        self.url_form = UrlInputForm(
            header_frame,
            on_submit=self.handle_url_submitted,
            bg_color=self.theme_data["CTkFrame"]["fg_color"],
        )
        self.url_form.grid(row=2, column=0, sticky=ctk.EW, pady=(8, 0), padx=8)

        url_horizontal_divider = Divider(
            header_frame, orientation="horizontal", thickness=2
        )
        url_horizontal_divider.grid_horizontal(row=3, column=0, pady=(4, 4), padx=8)

        content_frame = ctk.CTkFrame(
            self, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        content_frame.grid(row=1, column=0, sticky=ctk.NSEW, pady=(0, 8))
        content_frame.grid_columnconfigure(0, weight=0)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)

        self.left_frame = ctk.CTkFrame(
            content_frame, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        self.left_frame.grid(row=0, column=0, sticky=ctk.NSEW, padx=(16, 0))

        self.right_frame = ctk.CTkFrame(
            content_frame, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        self.right_frame.grid(row=0, column=1, sticky=ctk.NSEW, padx=(0, 16))
        self.option_panel(self.left_frame)
        self.output_panel(self.right_frame)

    def option_panel(self, parent: ctk.CTkFrame):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(
            parent, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        self.header_frame.grid(row=0, column=0, sticky=ctk.EW)
        self.header_frame.grid_columnconfigure(0, weight=1)

        # Title section
        title_label = ctk.CTkLabel(
            self.header_frame,
            text="AAS Checklist options",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=self.theme_data["CTkLabel"]["fg_color"],
        )
        title_label.grid(row=0, column=0, sticky=ctk.W, padx=16)

        default_button = DefaultButton(
            self.header_frame,
            on_click=self.reset_default_options,
            default_options=self.default_options,
            bg_color=self.theme_data["CTkFrame"]["fg_color"],
        )
        default_button.grid(row=0, column=2, sticky=ctk.E)

        self._collapsed_container()

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
        self.output_box = LogBox(
            parent,
            log_queue=self.log_handler,
            bg_color=self.theme_data["CTkFrame"]["fg_color"],
            width=720,
        )
        self.output_box.grid(row=1, column=0, sticky=ctk.NSEW, padx=8, pady=8)

        # button section
        buttons_frame = ctk.CTkFrame(
            parent, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        buttons_frame.grid(row=1, column=1, sticky=ctk.NE, pady=(0, 8), padx=(4, 0))

        self.run_button = TestExecuteButton(
            buttons_frame,
            on_test=lambda: self.handle_run_test(
                files=self._files,
                api=self._url,
                kosmo_options={
                    key: value
                    for key, value in self.chosen_options.items()
                    if key in {k for k in self.kosmo.copy_chosen_options.keys()}
                    and value == True
                },
                idta_options={
                    key: value
                    for key, value in self.chosen_options.items()
                    if key in {k for k in self.idta.copy_chosen_options.keys()}
                    and value == True
                },
            ),
        )
        self.run_button.grid(row=0, column=0, sticky=ctk.E, pady=8)

        self.file_exporter = FileExporter(
            buttons_frame,
            on_export=lambda: self.handle_export_test_results(),
        )
        self.file_exporter.grid(row=1, column=0, sticky=ctk.E, pady=(0, 8))

        clear_button = ClearButton(buttons_frame, on_click=self.handle_clear_output)
        clear_button.grid(row=2, column=0, sticky=ctk.E, pady=(0, 8))

    def _collapsed_container(self):
        self.options_container = ctk.CTkFrame(
            self.left_frame,
            border_width=1,
            corner_radius=6,
            fg_color=self.theme_data["CTkFrame"]["fg_color"],
        )
        self.options_container.grid(
            row=1, column=0, columnspan=3, sticky=ctk.NSEW, padx=(0, 8), pady=(0, 8)
        )
        self.options_container.grid_columnconfigure(0, weight=1)

        # IDTA section
        self.idta_label = ctk.CTkLabel(
            self.options_container,
            text="IDTA",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.idta_label.grid(row=0, column=0, sticky=ctk.W, pady=(8, 0), padx=16)

        self.idta = IdtaOptions(
            self.options_container,
            on_check=self.handle_checkbox_options_changed,
            on_expanded=self.handle_expanded,
            chosen_options=self.chosen_options,
            default_options=self.default_options,
            expanded_states=self.expanded_states,
        )
        self.idta.grid(row=1, column=0, sticky=ctk.EW, pady=8, padx=16)

        self.idta_divider = Divider(
            self.options_container, orientation="horizontal", thickness=2
        )
        self.idta_divider.grid_horizontal(row=2, column=0, sticky=ctk.EW)

        # KOSMO section
        self.kosmo_label = ctk.CTkLabel(
            self.options_container,
            text="KOSMO",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.kosmo_label.grid(row=3, column=0, sticky=ctk.W, pady=(8, 0), padx=16)

        self.kosmo = KosmoOptions(
            self.options_container,
            on_check=self.handle_checkbox_options_changed,
            on_expanded=self.handle_expanded,
            chosen_options=self.chosen_options,
            default_options=self.default_options,
            expanded_states=self.expanded_states,
        )
        self.kosmo.grid(row=4, column=0, sticky=ctk.EW, pady=8, padx=16)

    def handle_file_selected(self, file_paths: List[str]):
        self._files = file_paths

    def handle_url_submitted(self, url: str):
        self._url = url

    def handle_run_test(self, **kwargs: Any):
        idta_options = kwargs.get("idta_options", {})
        kosmo_options = kwargs.get("kosmo_options", {})
        files: Optional[List[str]] = kwargs.get("files", [])
        api: Optional[str] = kwargs.get("api", "")

        idta_options[IDTA.all_aasd.name] = self.idta.aasd.is_all.get()
        idta_options[IDTA.all_aasc_3a.name] = self.idta.aasc_3a.is_all.get()

        for file in files:
            test = TestFileVerficator(
                file=file,
                stop_event=self.run_button.stop_event,
                kosmo_options=kosmo_options,
                idta_options=idta_options,
            )
            test.verify()

        if not api:
            return

    def handle_export_test_results(self):
        pass

    def handle_clear_output(self):
        self.output_box.clear()

    def handle_checkbox_options_changed(self, options: Dict[str, bool]):
        self.chosen_options.update(options)

    def handle_expanded(self, state: Tuple[str, bool]):
        name, expanded = state
        for section in self.expanded_states.keys():
            checkbox: TreeCheckboxFrame = None

            if section != name:
                self.expanded_states[section] = False

            if section in self.idta_group:
                checkbox = getattr(self.idta, section)
            elif section in self.kosmo_group:
                checkbox = getattr(self.kosmo, section)

            if section != name and checkbox.expanded:
                checkbox._toggle_items_visibility(trigger_callback=False)

        self.expanded_states[name] = expanded

    def reset_default_options(self, default_options: Dict[str, bool]):
        self.chosen_options = default_options.copy()
        self.idta.init_checkboxes()
        self.kosmo.init_checkboxes()
