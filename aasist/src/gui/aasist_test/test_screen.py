from typing import Dict, List
import customtkinter as ctk

from aasist.src.gui.aasist_test.options import IdtaOptions, KosmoOptions, UrlInputForm
from aasist.src.gui.common.clear_button import ClearButton
from aasist.src.gui.common.default_button import DefaultButton
from aasist.src.gui.common.divider import Divider
from aasist.src.gui.common.file_exporter import FileExporter
from aasist.src.gui.common.file_selector import FileSelector
from aasist.src.gui.common.log_box import LogBox
from aasist.src.gui.handler import _TEST_LOG_NAME, QueueHandler


class TestScreen(ctk.CTkFrame):
    default_options = {
        "standard": True,
        "ignore_optional_constraints": False,
        "check_id_short": True,
        "check_IRDI_or_IRI": True,
        "check_sumbodel_component": True,
        "check_cd_rules": True,
        "check_kind_type": True,
        "check_thumbnail": True,
        "checl_exist_value": False,
        "check_cd_mapping": False,
    }

    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent)
        self.parent = parent
        self.chosen_options: Dict[str, bool] = self.default_options.copy()
        self.theme_data = ctk.ThemeManager.theme
        self.log_handler = QueueHandler(_TEST_LOG_NAME)
        self.layout()

    def layout(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        browse_frame = ctk.CTkFrame(
            self, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        browse_frame.grid(row=0, column=0, sticky=ctk.EW)
        browse_frame.grid_columnconfigure(0, weight=1)

        self.file_selector = FileSelector(
            browse_frame,
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
            browse_frame, orientation="horizontal", thickness=2
        )
        file_horizontal_divider.grid_horizontal(row=1, column=0, pady=(4, 4), padx=8)

        self.url_form = UrlInputForm(
            browse_frame,
            on_submit=self.handle_url_submitted,
            bg_color=self.theme_data["CTkFrame"]["fg_color"],
        )
        self.url_form.grid(row=2, column=0, sticky=ctk.EW, pady=(8, 0), padx=8)

        url_horizontal_divider = Divider(self, orientation="horizontal", thickness=2)
        url_horizontal_divider.grid_horizontal(row=3, column=0, pady=(4, 4), padx=8)

        content_frame = ctk.CTkFrame(
            self, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        content_frame.grid(row=4, column=0, sticky=ctk.NSEW, pady=(0, 8))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_columnconfigure(2, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(
            content_frame, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        left_frame.grid(row=0, column=0, sticky=ctk.NSEW, padx=(16, 0))

        right_frame = ctk.CTkFrame(
            content_frame, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        right_frame.grid(row=0, column=2, sticky=ctk.NSEW, padx=(0, 16))

        self.option_panel(left_frame)
        self.output_panel(right_frame)

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
            text="AAS Checklist options",
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

        # IDTA section
        idta_label = ctk.CTkLabel(
            options_container,
            text="IDTA",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        idta_label.grid(row=0, column=0, sticky=ctk.W, pady=(8, 0), padx=16)

        self.idta_options = IdtaOptions(
            options_container,
            on_check=self.handle_checkbox_options_changed,
            chosen_options=self.chosen_options,
            default_options=self.default_options,
            bg_color="#ededed",
        )
        self.idta_options.grid(row=1, column=0, sticky=ctk.W, pady=8, padx=16)

        idta_divider = Divider(options_container, orientation="horizontal", thickness=2)
        idta_divider.grid_horizontal(row=2, column=0, sticky=ctk.EW)

        # KOSMO section
        kosmo_label = ctk.CTkLabel(
            options_container,
            text="KOSMO",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        kosmo_label.grid(row=3, column=0, sticky=ctk.W, pady=4, padx=16)

        self.kosmo_options = KosmoOptions(
            options_container,
            on_check=self.handle_checkbox_options_changed,
            chosen_options=self.chosen_options,
            default_options=self.default_options,
            bg_color="#ededed",
        )
        self.kosmo_options.grid(row=4, column=0, sticky=ctk.W, pady=8, padx=16)

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
        )
        self.output_box.grid(row=1, column=0, sticky=ctk.NSEW, padx=8, pady=8)

        # button section
        buttons_frame = ctk.CTkFrame(
            parent, fg_color=self.theme_data["CTkFrame"]["fg_color"]
        )
        buttons_frame.grid(row=1, column=1, sticky=ctk.NE, pady=(0, 8), padx=(4, 0))

        run_button = ctk.CTkButton(
            buttons_frame,
            text="Run Test",
            command=lambda: self.handle_run_test(
                # TODO: add parameters
            ),
            width=160,
            font=ctk.CTkFont(size=18, weight="normal"),
        )
        run_button.grid(
            row=0,
            column=0,
            sticky=ctk.E,
            pady=8,
            ipady=8,
        )

        self.file_exporter = FileExporter(
            buttons_frame,
            on_export=self.handle_export_test_results,
        )
        self.file_exporter.grid(row=1, column=0, sticky=ctk.E, pady=(0, 8))

        clear_button = ClearButton(buttons_frame, on_click=self.handle_clear_output)
        clear_button.grid(row=2, column=0, sticky=ctk.E, pady=(0, 8))

    def handle_file_selected(self, file_paths: List[str]):
        pass

    def handle_url_submitted(self, url: str):
        print(f"URL submitted: {url}")

    def handle_run_test(self, **kwargs):
        pass

    def handle_export_test_results(self):
        pass

    def handle_clear_output(self):
        self.output_box.clear()

    def handle_checkbox_options_changed(self, options: Dict[str, bool]):
        self.chosen_options.update(options)

    def reset_default_options(self, default_options: Dict[str, bool]):
        self.chosen_options = default_options.copy()
        self.idta_options.init_checkboxes()
        self.kosmo_options.init_checkboxes()
