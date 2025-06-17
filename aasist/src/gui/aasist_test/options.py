from typing import Callable, Dict
import customtkinter as ctk


class UrlInputForm(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        on_submit: Callable[[str], None],
        bg_color: str = None,
    ):
        super().__init__(parent, fg_color=bg_color)
        self.on_submit = on_submit

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self._placeholder = "Enter server API... eg.) https://admin-shell.io/aas/API/3/0/AssetAdministrationShellRepositoryServiceSpecification/SSP-002"

        confirm_button = ctk.CTkButton(
            self,
            text="Connect",
            command=self.confirm,
            width=120,
            font=ctk.CTkFont(size=14, weight="normal"),
        )
        confirm_button.grid(row=0, column=0, padx=8, pady=8, ipady=8, sticky=ctk.W)

        self.form = ctk.CTkTextbox(
            self,
            height=40,
            wrap="none",
            state=ctk.NORMAL,
            font=ctk.CTkFont(size=16, weight="normal"),
        )
        self.form._textbox.configure(padx=8, pady=8)
        self.form.configure(text_color="gray")
        self.form.insert("1.0", self._placeholder)
        self.form.grid(row=0, column=1, sticky=ctk.EW, padx=8)
        self.form.bind("<FocusIn>", self.on_focus_in)
        self.form.bind("<FocusOut>", self.on_focus_out)

    def confirm(self):
        input = self.form.get("1.0", ctk.END)
        input = input if input.strip() != self._placeholder else ""
        self.on_submit(input.strip())

    def on_focus_in(self, event):
        if self.form.get("1.0", ctk.END).strip() == self._placeholder.strip():
            self.form.delete("1.0", ctk.END)
            self.form.configure(text_color="black")

    def on_focus_out(self, event):
        if not self.form.get("1.0", ctk.END).strip():
            self.form.insert("1.0", self._placeholder)
            self.form.configure(text_color="gray")
        else:
            self.form.configure(text_color="black")


class IdtaOptions(ctk.CTkFrame):
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
        self.idta_options = [
            ("standard", "표준 검사"),
            ("ignore_optional_constraints", "권장 제약 조건 무시"),
        ]
        self.copy_chosen_options: Dict[str, ctk.BooleanVar] = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {k for k, _ in self.idta_options}
        }
        self.grid_columnconfigure(0, weight=1)

        STANDARD_INDEX = 0
        IGNORE_OPTIONAL_INDEX = 1

        idta_standard = ctk.CTkCheckBox(
            self,
            text=self.idta_options[STANDARD_INDEX][-1],
            variable=self.copy_chosen_options["standard"],
            command=self._callback,
            font=ctk.CTkFont(size=16),
            width=16,
            height=16,
        )
        idta_standard.grid(row=0, column=0, sticky=ctk.W, padx=12, pady=(8, 0))
        idta_standard_desc = ctk.CTkLabel(
            self,
            text="IDTA 표준에 따른 참조모델의 제약조건을 검사합니다",
            font=ctk.CTkFont(size=14),
            text_color="#9C9C9C",
        )
        idta_standard_desc.grid(row=1, column=0, sticky=ctk.W, ipadx=44, pady=(0, 8))

        ignore_optional_constraints = ctk.CTkCheckBox(
            self,
            text=self.idta_options[IGNORE_OPTIONAL_INDEX][-1],
            variable=self.copy_chosen_options["ignore_optional_constraints"],
            command=self._callback,
            font=ctk.CTkFont(size=16),
            width=16,
            height=16,
        )
        ignore_optional_constraints.grid(
            row=2, column=0, sticky=ctk.W, padx=12, pady=(8, 0)
        )
        ignore_optional_constraints_desc = ctk.CTkLabel(
            self,
            text="필수가 아닌 제약조건을 무시합니다",
            font=ctk.CTkFont(size=14),
            text_color="#9C9C9C",
        )
        ignore_optional_constraints_desc.grid(
            row=3, column=0, sticky=ctk.W, ipadx=44, pady=(0, 8)
        )

    def init_checkboxes(self):
        for key, var in self.copy_chosen_options.items():
            var.set(self.default_options[key])
        self._callback()

    def _callback(self):
        result = {k: v.get() for k, v in self.copy_chosen_options.items()}
        self.on_check(result)


class KosmoOptions(ctk.CTkFrame):
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
        self.idta_options = [
            ("check_id_short", "idShort 설정/명명 규칙 검사"),
            ("check_IRDI_or_IRI", "IRDI/IRI 형식 검사"),
            ("check_sumbodel_component", "Submodel 구성 검사"),
            ("check_cd_rules", "Concept Description 규칙 검사"),
            ("check_kind_type", "Kind 유형 검사"),
            ("check_thumbnail", "Thumbnail 이미지 확인"),
            ("checl_exist_value", "Value 값 존재 여부 확인"),
            ("check_cd_mapping", "Concept Description Mapping 확인"),
        ]
        self._sub_description = [
            ("check_id_short", "idShort가 대문자로 시작하는지 검사합니다"),
            ("check_IRDI_or_IRI", "Id가 IRDI/IRI 형식을 준수하는지 검사합니다"),
            ("check_sumbodel_component", "필수 Submodel 4종을 포함하는지 검사합니다"),
            ("check_cd_rules", "Concept Description 관련 규칙을 검사합니다"),
            ("check_kind_type", "Kind 유형이 올바르게 설정되었는지 검사합니다"),
            ("check_thumbnail", "Thumbnail 이미지가 존재하는지 검사합니다"),
            ("checl_exist_value", "Property의 Value가 빈 값인지 확인합니다"),
            (
                "check_cd_mapping",
                "SubmodelElementCollection과 ConceptDescription의 매핑 여부를 확인합니다",
            ),
        ]
        self.copy_chosen_options: Dict[str, ctk.BooleanVar] = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {k for k, _ in self.idta_options}
        }

        self.grid_columnconfigure(0, weight=1)

        desc_row = 0
        for i, (key, label) in enumerate(self.idta_options):
            check_row = i
            if i > 0:
                check_row = desc_row + 1
            check_box = ctk.CTkCheckBox(
                self,
                text=label,
                variable=self.copy_chosen_options[key],
                command=self._callback,
                font=ctk.CTkFont(size=16),
                width=16,
                height=16,
            )
            check_box.grid(row=check_row, column=0, sticky=ctk.W, padx=12, pady=(8, 0))

            description = ctk.CTkLabel(
                self,
                text=self._sub_description[i][-1],
                font=ctk.CTkFont(size=14),
                text_color="#9C9C9C",
            )
            desc_row = check_row + 1
            description.grid(
                row=desc_row, column=0, sticky=ctk.W, ipadx=44, pady=(0, 8)
            )

    def init_checkboxes(self):
        for key, var in self.copy_chosen_options.items():
            var.set(self.default_options[key])
        self._callback()

    def _callback(self):
        result = {k: v.get() for k, v in self.copy_chosen_options.items()}
        self.on_check(result)
