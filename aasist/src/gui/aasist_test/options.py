import threading
from typing import Any, Callable, Dict, List, Tuple
import customtkinter as ctk

from aasist.src.gui.common.tree_checkbox_frame import TreeCheckboxFrame
from aasist.src.module.tester.constants import IDTA, KOSMO


class TestExecuteButton(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        on_test: Callable,
        bg_color: str = "#F2F2F2",
        **kwargs
    ):
        super().__init__(parent, fg_color=bg_color)

        self.on_test = on_test
        self.stop_event = threading.Event()
        self.is_processing = False

        self.run_button = ctk.CTkButton(
            self,
            text="Run Test",
            command=lambda: self.start(**kwargs),
            width=160,
            font=ctk.CTkFont(size=18, weight="normal"),
        )
        self.run_button.grid(row=0, column=0, pady=(0, 4), ipady=8, sticky=ctk.E)

    def run_test(self, **kwargs: Any):
        self.on_test(**kwargs)
        self.is_processing = False
        self.after(0, self.reset_button_state, "Run Test")

    def start(self, **kwargs: Any):
        if self.is_processing:
            self.stop()
            return
        self.is_processing = True
        self.stop_event.clear()
        self.reset_button_state("Stop Test")
        self.thread = threading.Thread(target=self.run_test, args=(kwargs), daemon=True)
        self.thread.start()

    def stop(self):
        if self.is_processing:
            self.stop_event.set()
            self.is_processing = False
            self.reset_button_state("Run Test")

    def reset_button_state(self, text: str):
        self.run_button.configure(text=text)


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
        on_expanded: Callable[[Tuple[str, bool]], None],
        chosen_options: Dict[str, bool],
        expanded_states: Dict[str, bool] = None,
        default_options: Dict[str, bool] = None,
        bg_color: str = "#F2F2F2",
    ):
        super().__init__(parent, fg_color=bg_color)
        self.bg_color = bg_color
        self.on_check = on_check
        self.on_expanded = on_expanded
        self.default_options = default_options
        self.expanded_states: Dict[str, bool] = {
            k: v for k, v in expanded_states.items() if k in {"idta", "aasd", "aasc_3a"}
        }
        self.idta_options = [
            {
                "key": IDTA.standard.name,
                "label": "표준 검사",
                "description": "IDTA 표준에 따른 참조모델의 제약조건을 검사합니다",
            },
            {
                "key": IDTA.optional.name,
                "label": "느슨한 표준 검사",
                "description": "AAS 뷰어에서 정상적으로 조회되는 경우 표준을 준수했다고 간주합니다",
            },
        ]
        self.part1_constraints = [
            {
                "key": IDTA.aasd_002.name,
                "label": "AASd-002 제약조건 검사",
            },
            {
                "key": IDTA.aasd_005.name,
                "label": "AASd-005 제약조건 검사",
            },
            {
                "key": IDTA.aasd_006.name,
                "label": "AASd-006 제약조건 검사",
            },
            {
                "key": IDTA.aasd_014.name,
                "label": "AASd-014 제약조건 검사",
            },
            {
                "key": IDTA.aasd_022.name,
                "label": "AASd-022 제약조건 검사",
            },
            {
                "key": IDTA.aasd_090.name,
                "label": "AASd-090 제약조건 검사",
            },
            {
                "key": IDTA.aasd_107.name,
                "label": "AASd-107 제약조건 검사",
            },
            {
                "key": IDTA.aasd_109.name,
                "label": "AASd-109 제약조건 검사",
            },
            {
                "key": IDTA.aasd_114.name,
                "label": "AASd-114 제약조건 검사",
            },
            {
                "key": IDTA.aasd_116.name,
                "label": "AASd-116 제약조건 검사",
            },
            {
                "key": IDTA.aasd_117.name,
                "label": "AASd-117 제약조건 검사",
            },
            {
                "key": IDTA.aasd_118.name,
                "label": "AASd-118 제약조건 검사",
            },
            {
                "key": IDTA.aasd_119.name,
                "label": "AASd-119 제약조건 검사",
            },
            {
                "key": IDTA.aasd_120.name,
                "label": "AASd-120 제약조건 검사",
            },
            {
                "key": IDTA.aasd_121.name,
                "label": "AASd-121 제약조건 검사",
            },
            {
                "key": IDTA.aasd_122.name,
                "label": "AASd-122 제약조건 검사",
            },
            {
                "key": IDTA.aasd_123.name,
                "label": "AASd-123 제약조건 검사",
            },
            {
                "key": IDTA.aasd_124.name,
                "label": "AASd-124 제약조건 검사",
            },
            {
                "key": IDTA.aasd_125.name,
                "label": "AASd-125 제약조건 검사",
            },
            {
                "key": IDTA.aasd_126.name,
                "label": "AASd-126 제약조건 검사",
            },
            {
                "key": IDTA.aasd_127.name,
                "label": "AASd-127 제약조건 검사",
            },
            {
                "key": IDTA.aasd_129.name,
                "label": "AASd-129 제약조건 검사",
            },
            {
                "key": IDTA.aasd_130.name,
                "label": "AASd-130 제약조건 검사",
            },
            {
                "key": IDTA.aasd_131.name,
                "label": "AASd-131 제약조건 검사",
            },
            {
                "key": IDTA.aasd_133.name,
                "label": "AASd-133 제약조건 검사",
            },
            {
                "key": IDTA.aasd_134.name,
                "label": "AASd-134 제약조건 검사",
            },
        ]
        self.part3a_constraints = [
            {
                "key": IDTA.aasc_3a_002.name,
                "label": "AASc-3a-002 제약조건 검사",
            },
            {
                "key": IDTA.aasc_3a_004.name,
                "label": "AASc-3a-004 제약조건 검사",
            },
            {
                "key": IDTA.aasc_3a_005.name,
                "label": "AASc-3a-005 제약조건 검사",
            },
            {
                "key": IDTA.aasc_3a_006.name,
                "label": "AASc-3a-006 제약조건 검사",
            },
            {
                "key": IDTA.aasc_3a_007.name,
                "label": "AASc-3a-007 제약조건 검사",
            },
            {
                "key": IDTA.aasc_3a_008.name,
                "label": "AASc-3a-008 제약조건 검사",
            },
            {
                "key": IDTA.aasc_3a_009.name,
                "label": "AASc-3a-009 제약조건 검사",
            },
            {
                "key": IDTA.aasc_3c_010.name,
                "label": "AASc-3c-010 제약조건 검사",
            },
        ]

        idta_choices = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {m.get("key") for m in self.idta_options}
        }
        aasd_choices = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {m.get("key") for m in self.part1_constraints}
        }
        aasc_3a_choices = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {m.get("key") for m in self.part3a_constraints}
        }

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.idta = TreeCheckboxFrame(
            self,
            title="표준 검증",
            chosen_options=idta_choices,
            items=self.idta_options,
            on_check=self.check,
            on_expanded=lambda expanded: self.expand("idta", expanded),
            default_options=default_options,
            is_expanded=self.expanded_states.get("idta", True),
        )
        self.idta.grid(row=0, column=0, sticky=ctk.NSEW, pady=(8, 0))

        self.aasd = TreeCheckboxFrame(
            self,
            title="Part 1. Check AASd",
            chosen_options=aasd_choices,
            items=self.part1_constraints,
            on_check=self.check,
            on_expanded=lambda expanded: self.expand("aasd", expanded),
            default_options=default_options,
            is_expanded=self.expanded_states.get("aasd", False),
        )
        self.aasd.grid(row=1, column=0, sticky=ctk.NSEW, pady=8)

        self.aasc_3a = TreeCheckboxFrame(
            self,
            title="Part 3. Check AASc-3a",
            chosen_options=aasc_3a_choices,
            items=self.part3a_constraints,
            on_check=self.check,
            on_expanded=lambda expanded: self.expand("aasc_3a", expanded),
            default_options=default_options,
            is_expanded=self.expanded_states.get("aasc_3a", False),
        )

        self.aasc_3a.grid(row=2, column=0, sticky=ctk.NSEW, pady=(0, 8))

    def check(self, options: Dict[str, bool]):
        # TODO
        self.on_check(options)

    def init_checkboxes(self):
        self.idta.init()
        self.aasd.init()
        self.aasc_3a.init()

    def expanded_with_height(self) -> List[Tuple[bool, int, int]]:
        return [
            (self.idta.expanded, 180, 180),
            (self.aasd.expanded, 27, 255),
            (self.aasc_3a.expanded, 27, 255),
        ]

    def expand(self, option_name: str, expanded: bool):
        self.expanded_states[option_name] = expanded
        self.on_expanded((option_name, expanded))


class KosmoOptions(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        on_check: Callable[[Dict[str, bool]], None],
        on_expanded: Callable[[Tuple[str, bool]], None],
        chosen_options: Dict[str, bool],
        expanded_states: Dict[str, bool] = None,
        default_options: Dict[str, bool] = None,
        bg_color: str = "#F2F2F2",
    ):
        super().__init__(parent, fg_color=bg_color)
        self.bg_color = bg_color
        self.on_check = on_check
        self.on_expanded = on_expanded
        self.default_options = default_options
        self.expanded_states: Dict[str, bool] = {
            k: v
            for k, v in expanded_states.items()
            if k
            in {"kosmo_aas", "kosmo_submodel", "kosmo_smc", "kosmo_prop", "kosmo_cd"}
        }
        self.kosmo_aas_options = [
            {
                "key": KOSMO.aas_thumbnail.name,
                "label": "Thumbnail 이미지 확인",
                "description": "파일이 Thumbnail 이미지를 포함하는지 확인합니다",
            },
            {
                "key": KOSMO.aas_id_short.name,
                "label": "idShort 설정/명명 규칙 검사",
                "description": "idShort가 대문자로 시작하는지 검사합니다",
            },
            {
                "key": KOSMO.aas_id.name,
                "label": "Id 형식 검사",
                "description": "Id가 IRI 형식을 준수하는지 검사합니다",
            },
            {
                "key": KOSMO.aas_submodel.name,
                "label": "Submodel 구성 검사",
                "description": "필수 Submodel 4종을 포함하는지 검사합니다",
            },
            {
                "key": KOSMO.aas_global_asset_id.name,
                "label": "globalAssetId 설정 검사",
                "description": "globalAssetId 설정 여부를 검사합니다",
            },
            {
                "key": KOSMO.aas_type.name,
                "label": "Type 유형 검사",
                "description": "kind가 Type으로 지정되었는지 확인합니다",
            },
        ]
        self.kosmo_submodel_options = [
            {
                "key": KOSMO.submodel_id_short.name,
                "label": "idShort 설정/명명 규칙 검사",
                "description": "idShort가 대문자로 시작하는지 검사합니다",
            },
            {
                "key": KOSMO.submodel_id.name,
                "label": "Id 형식 검사",
                "description": "Id가 IRI 형식을 준수하는지 검사합니다",
            },
            {
                "key": KOSMO.submodel_semantic_id.name,
                "label": "semanticId 설정/명명 규칙 검사",
                "description": "semanticId가 IRI 형식을 준수하는지 검사합니다",
            },
            {
                "key": KOSMO.submodel_kind.name,
                "label": "Kind 유형 검사",
                "description": "kind 유형이 올바르게 설정되었는지 검사합니다",
            },
        ]
        self.kosmo_smc_options = [
            {
                "key": KOSMO.smc_id_short.name,
                "label": "idShort 설정/명명 규칙 검사",
                "description": "idShort가 대문자로 시작하는지 검사합니다",
            },
            {
                "key": KOSMO.smc_cd_mapping.name,
                "label": "Concept Description Mapping 확인",
                "description": "ConceptDescription의 매핑 여부를 확인합니다",
            },
        ]
        self.kosmo_property_options = [
            {
                "key": KOSMO.prop_value.name,
                "label": "Value 값 존재 여부 확인",
                "description": "Property의 Value가 빈 값인지 확인합니다",
            },
            {
                "key": KOSMO.prop_id_short.name,
                "label": "idShort 설정/명명 규칙 검사",
                "description": "idShort가 대문자로 시작하는지 검사합니다",
            },
            {
                "key": KOSMO.prop_cd_mapping.name,
                "label": "Concept Description Mapping 확인",
                "description": "ConceptDescription의 매핑 여부를 확인합니다",
            },
        ]
        self.kosmo_cd_options = [
            {
                "key": KOSMO.cd_id_short.name,
                "label": "idShort 설정/명명 규칙 검사",
                "description": "idShort가 대문자로 시작하는지 검사합니다",
            },
            {
                "key": KOSMO.cd_id.name,
                "label": "Id 형식 검사",
                "description": "Id가 IRI 형식을 준수하는지 검사합니다",
            },
            {
                "key": KOSMO.cd_definition.name,
                "label": "definition 설정 검사",
                "description": "definition/description 설정 여부를 검사합니다",
            },
        ]

        aas_choices = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {m.get("key") for m in self.kosmo_aas_options}
        }

        submodel_choices = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {m.get("key") for m in self.kosmo_submodel_options}
        }

        smc_choices = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {m.get("key") for m in self.kosmo_smc_options}
        }
        property_choices = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {m.get("key") for m in self.kosmo_property_options}
        }

        cd_choices = {
            key: ctk.BooleanVar(self, value=value)
            for key, value in chosen_options.items()
            if key in {m.get("key") for m in self.kosmo_cd_options}
        }

        self.copy_chosen_options: Dict[str, bool] = {}
        self.copy_chosen_options.update(aas_choices)
        self.copy_chosen_options.update(submodel_choices)
        self.copy_chosen_options.update(smc_choices)
        self.copy_chosen_options.update(property_choices)
        self.copy_chosen_options.update(cd_choices)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.kosmo_aas = TreeCheckboxFrame(
            self,
            title="AAS 검증",
            chosen_options=aas_choices,
            items=self.kosmo_aas_options,
            on_check=self.check,
            on_expanded=lambda expanded: self.expand("kosmo_aas", expanded),
            default_options=default_options,
            is_expanded=self.expanded_states.get("kosmo_aas", True),
        )
        self.kosmo_aas.grid(row=0, column=0, sticky=ctk.NSEW, pady=(8, 0))

        self.kosmo_submodel = TreeCheckboxFrame(
            self,
            title="Submodel 검증",
            chosen_options=submodel_choices,
            items=self.kosmo_submodel_options,
            on_check=self.check,
            on_expanded=lambda expanded: self.expand("kosmo_submodel", expanded),
            default_options=default_options,
            is_expanded=self.expanded_states.get("kosmo_submodel", False),
        )
        self.kosmo_submodel.grid(row=1, column=0, sticky=ctk.NSEW, pady=(8, 0))

        self.kosmo_smc = TreeCheckboxFrame(
            self,
            title="SMC 검증",
            chosen_options=smc_choices,
            items=self.kosmo_smc_options,
            on_check=self.check,
            on_expanded=lambda expanded: self.expand("kosmo_smc", expanded),
            default_options=default_options,
            is_expanded=self.expanded_states.get("kosmo_smc", False),
        )

        self.kosmo_smc.grid(row=2, column=0, sticky=ctk.NSEW, pady=(8, 0))

        self.kosmo_prop = TreeCheckboxFrame(
            self,
            title="Property 검증",
            chosen_options=property_choices,
            items=self.kosmo_property_options,
            on_check=self.check,
            on_expanded=lambda expanded: self.expand("kosmo_prop", expanded),
            default_options=default_options,
            is_expanded=self.expanded_states.get("kosmo_prop", False),
        )

        self.kosmo_prop.grid(row=3, column=0, sticky=ctk.NSEW, pady=(8, 0))

        self.kosmo_cd = TreeCheckboxFrame(
            self,
            title="Concept Description 검증",
            chosen_options=cd_choices,
            items=self.kosmo_cd_options,
            on_check=self.check,
            on_expanded=lambda expanded: self.expand("kosmo_cd", expanded),
            default_options=default_options,
            is_expanded=self.expanded_states.get("kosmo_cd", False),
        )

        self.kosmo_cd.grid(row=4, column=0, sticky=ctk.NSEW, pady=(8, 0))

    def check(self, options: Dict[str, bool]):
        # TODO
        self.on_check(options)

    def init_checkboxes(self):
        self.kosmo_aas.init()
        self.kosmo_submodel.init()
        self.kosmo_smc.init()
        self.kosmo_prop.init()
        self.kosmo_cd.init()

    def expanded_with_height(self) -> List[Tuple[bool, int, int]]:
        return [
            (self.kosmo_aas.expanded, 27, 255),
            (self.kosmo_submodel.expanded, 27, 255),
            (self.kosmo_smc.expanded, 27, 255),
            (self.kosmo_prop.expanded, 27, 255),
            (self.kosmo_cd.expanded, 27, 255),
        ]

    def expand(self, option_name: str, expanded: bool):
        self.expanded_states[option_name] = expanded
        self.on_expanded((option_name, expanded))
