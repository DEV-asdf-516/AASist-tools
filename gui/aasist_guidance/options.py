from typing import Callable, Dict
import customtkinter as ctk


# 토글버튼
class FileFormatToggleButton(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, on_toggle: Callable[[str], None]):
        super().__init__(parent)
        self.on_toggle = on_toggle
        self.toggles = ["Word(.docx)", "Excel(.xlsx)"]
        self.chosen_option = self.toggles[0]
        self.toggle_button = ctk.CTkSegmentedButton(
            self,
            values=self.toggles,
            command=self._handle_changed,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=320,
            height=40,
        )

        self.toggle_button.grid(row=0, column=0, sticky=ctk.W)
        self.toggle_button.set(self.chosen_option)

    def _handle_changed(self, option: str):
        if self.chosen_option == option:
            return

        self.chosen_option = option
        self._callback(option)

    def init_buttons(self):
        self.chosen_option = self.toggles[0]
        self._callback(self.chosen_option)

    def _callback(self, option: str):
        self.toggle_button.set(self.chosen_option)
        self.on_toggle(option)


# 서브모델 옵션
class SubmodelOptions(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        on_check: Callable[[Dict[str, bool]], None],
        chosen_options: Dict[str, bool],
        bg_color: str = None,
    ):
        super().__init__(parent, fg_color=bg_color)
        self.on_check = on_check

        self.submodel_options = [
            ("all_submodels", "All"),
            ("identification", "Identification"),
            ("documentation", "Documentation"),
            ("cad", "CAD"),
            ("carbon_footprint", "CarbonFootprint"),
            ("hierarchical_structures", "HierarchicalStructures"),
            ("digital_nameplate", "DigitalNameplate"),
            ("technical_data", "TechnicalData"),
            ("operational_data", "OperationalData"),
            ("etc", "기타"),
        ]
        self.copy_chosen_options: Dict[str, ctk.BooleanVar] = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {k for k, _ in self.submodel_options}
        }

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i, (key, label) in enumerate(self.submodel_options):
            row_pos = i // 3
            col_pos = i % 3

            check_box = ctk.CTkCheckBox(
                self,
                text=label,
                variable=self.copy_chosen_options[key],
                command=lambda k=key: self._select_checkbox(k),  # late binding closure
                font=ctk.CTkFont(size=14),
                width=16,
                height=16,
            )
            check_box.grid(row=row_pos, column=col_pos, sticky=ctk.W, padx=12, pady=8)

    def _select_checkbox(self, option: str):
        if option == "all_submodels":
            [
                self.copy_chosen_options[k].set(self.copy_chosen_options[option].get())
                for k in self.copy_chosen_options
                if k != "all_submodels"
            ]
        elif self.copy_chosen_options["all_submodels"].get():
            self.copy_chosen_options["all_submodels"].set(False)
        self._callback()

    def init_checkboxes(self):
        for key, var in self.copy_chosen_options.items():
            var.set(True)

        self._callback()

    def _callback(self):
        result = {k: v.get() for k, v in self.copy_chosen_options.items()}
        self.on_check(result)


# 속성 옵션
class AttiributeOptions(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        on_check: Callable[[Dict[str, bool]], None],
        chosen_options: Dict[str, bool],
        default_options: Dict[str, bool] = None,
        bg_color: str = None,
    ):
        super().__init__(parent, fg_color=bg_color)
        self.on_check = on_check
        self.default_options = default_options
        self.attribute_options = [
            ("all_attributes", "All"),
            ("model_type", "메타 모델"),
            ("id_short", "idShort"),
            ("semantic_id", "Semantic ID"),
            ("depth", "SMC Hierarchy"),
            ("definition", "정의(IEC61360)"),
            ("description", "설명"),
            ("value", "Value"),
            ("value_type", "Value Type"),
            ("reference_type", "참조유형"),
        ]

        self.copy_chosen_options: Dict[str, ctk.BooleanVar] = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {k for k, _ in self.attribute_options}
        }

        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        for i, (key, label) in enumerate(self.attribute_options):
            row_pos = i // 3
            col_pos = i % 3

            check_box = ctk.CTkCheckBox(
                self,
                text=label,
                variable=self.copy_chosen_options[key],
                command=lambda k=key: self._select_checkbox(k),  # late binding closure
                font=ctk.CTkFont(size=14),
                width=16,
                height=16,
            )
            check_box.grid(row=row_pos, column=col_pos, sticky=ctk.W, padx=12, pady=8)

    def _select_checkbox(self, option: str):
        if option == "all_attributes":
            [
                self.copy_chosen_options[k].set(self.copy_chosen_options[option].get())
                for k in self.copy_chosen_options
                if k != "all_attributes"
            ]
        elif self.copy_chosen_options["all_attributes"].get():
            self.copy_chosen_options["all_attributes"].set(False)
        self._callback()

    def init_checkboxes(self):
        for key, var in self.copy_chosen_options.items():
            var.set(self.default_options[key])

        self._callback()

    def _callback(self):
        result = {k: v.get() for k, v in self.copy_chosen_options.items()}
        self.on_check(result)


class SettingOptions(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        on_check: Callable[[Dict[str, bool]], None],
        chosen_options: Dict[str, bool],
        default_options: Dict[str, bool],
        bg_color: str = None,
    ):
        super().__init__(parent, fg_color=bg_color)

        self.on_check = on_check
        self.default_options = default_options
        self.setting_options = [
            ("simple_model_type", "메타모델을 약어로 표시"),
            ("depth_ellipses", "가이던스 표 형식 적용"),
        ]
        self.copy_chosen_options: Dict[str, ctk.BooleanVar] = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {k for k, _ in self.setting_options}
        }

        self.grid_columnconfigure(0, weight=1)

        USE_SIMPLE_TYPE_INDEX = 0
        HIERARCHY_ELLIPSES_INDEX = 1

        use_simple_type = ctk.CTkCheckBox(
            self,
            text=self.setting_options[USE_SIMPLE_TYPE_INDEX][-1],
            variable=self.copy_chosen_options["simple_model_type"],
            command=self._callback,
            font=ctk.CTkFont(size=16),
            width=16,
            height=16,
        )

        use_simple_type.grid(row=0, column=0, sticky=ctk.W, padx=12, pady=(8, 0))
        use_simple_type_desc = ctk.CTkLabel(
            self,
            text="메타모델을 약어로 표시합니다  예) Property -> Prop",
            font=ctk.CTkFont(size=14),
            text_color="#9C9C9C",
        )
        use_simple_type_desc.grid(row=1, column=0, sticky=ctk.W, ipadx=44, pady=(0, 8))

        hierarchy_ellipses = ctk.CTkCheckBox(
            self,
            text=self.setting_options[HIERARCHY_ELLIPSES_INDEX][-1],
            variable=self.copy_chosen_options["depth_ellipses"],
            command=self._callback,
            font=ctk.CTkFont(size=16),
            width=16,
            height=16,
        )

        hierarchy_ellipses.grid(row=2, column=0, sticky=ctk.W, padx=12, pady=(8, 0))
        hierarchy_ellipses_desc = ctk.CTkLabel(
            self,
            text="계층 트리를 평탄화하여 표시합니다",
            font=ctk.CTkFont(size=14),
            text_color="#9C9C9C",
        )
        hierarchy_ellipses_desc.grid(
            row=3, column=0, sticky=ctk.W, ipadx=44, pady=(0, 8)
        )

    def init_checkboxes(self):
        for key, var in self.copy_chosen_options.items():
            var.set(self.default_options[key])
        self._callback()

    def _callback(self):
        result = {k: v.get() for k, v in self.copy_chosen_options.items()}
        self.on_check(result)
