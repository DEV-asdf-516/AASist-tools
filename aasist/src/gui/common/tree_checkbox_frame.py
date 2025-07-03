from typing import Callable, Dict, List
import customtkinter as ctk


class TreeCheckboxFrame(ctk.CTkFrame):

    def __init__(
        self,
        parent: ctk.CTkFrame,
        title: str,
        items: List[Dict],
        chosen_options: Dict[str, ctk.BooleanVar],
        on_check: Callable,
        on_expanded: Callable,
        default_options: Dict[str, bool] = {},
        is_expanded: bool = True,
        bg_color: str = "#F2F2F2",
        font_size: int = 18,
        max_height: int = 200,
        left_padding: int = 8,
    ):
        super().__init__(parent)
        self.title = title
        self.items = items
        self.chosen_options = chosen_options
        self.default_options = default_options
        self.on_check = on_check
        self.on_expanded = on_expanded
        self.expanded = is_expanded
        self.font_size = font_size
        self.bg_color = bg_color
        self.max_height = max_height
        self.left_padding = left_padding

        self.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color=bg_color)
        self.header_frame.grid(row=0, column=0, sticky=ctk.EW, padx=4)

        self.header_frame.grid_columnconfigure(0, minsize=480, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)

        self.is_all = ctk.BooleanVar(value=False)

        self.title_check_box = ctk.CTkCheckBox(
            self.header_frame,
            text=self.title,
            font=ctk.CTkFont(size=font_size, weight="bold"),
            command=self._all_options,
            width=16,
            height=16,
            variable=self.is_all,
        )

        self.title_check_box.grid(row=0, column=0, sticky=ctk.W)

        self.visibility_button = ctk.CTkButton(
            self.header_frame,
            text="▼" if self.expanded else "▲",
            command=self._toggle_items_visibility,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=24,
            height=24,
        )
        self.visibility_button.grid(row=0, column=1, sticky=ctk.W, padx=8)

        estimated_height = 0

        for item in self.items:
            estimated_height += self.font_size
            if item.get("description"):
                estimated_height = estimated_height + self.font_size - 2
                estimated_height += 8
            estimated_height += 8

        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=6, width=500)
        self.normal_frame = ctk.CTkFrame(self, corner_radius=6)

        self.content_frame = (
            self.scrollable_frame
            if estimated_height > self.max_height
            else self.normal_frame
        )

        if self.expanded:
            self.content_frame.grid(row=1, column=0, sticky=ctk.EW, pady=8, padx=4)
            min_size = (
                350 if isinstance(self.content_frame, ctk.CTkScrollableFrame) else 0
            )
            self.content_frame.grid_rowconfigure(0, minsize=min_size, weight=1)

        self._checkboxes(self.items)

        self.content_frame.grid_columnconfigure(0, minsize=500, weight=1)

    def _toggle_items_visibility(self, trigger_callback: bool = True):
        if self.expanded:
            self.content_frame.grid_remove()
            self.visibility_button.configure(text="▲")
            self.expanded = False
        else:
            self.content_frame.grid(row=1, column=0, sticky=ctk.EW, pady=8, padx=4)
            self.visibility_button.configure(text="▼")
            self.expanded = True
        if trigger_callback:
            self.on_expanded(self.expanded)

    def _checkboxes(self, items: List[Dict]):
        # 플리커링 감소
        widgets = []
        row = 0
        for i, item in enumerate(items):
            check_row = row + 1 if i > 0 else i
            key = item["key"]
            if key in self.chosen_options:
                check_box = ctk.CTkCheckBox(
                    self.content_frame,
                    text=item["label"],
                    variable=self.chosen_options[key],
                    command=self._select_checkbox,
                    font=ctk.CTkFont(size=self.font_size - 2),
                    width=16,
                    height=16,
                )
                widgets.append(
                    {
                        "widget": check_box,
                        "grid_args": {
                            "row": check_row,
                            "column": 0,
                            "sticky": ctk.EW,
                            "padx": 12 + self.left_padding,
                            "pady": 8,
                        },
                    }
                )
            if item.get("description"):
                sub_label = ctk.CTkLabel(
                    self.content_frame,
                    text=item["description"],
                    font=ctk.CTkFont(size=self.font_size - 3),
                    text_color="gray",
                    corner_radius=6,
                )
                row = check_row + 1
                widgets.append(
                    {
                        "widget": sub_label,
                        "grid_args": {
                            "row": row,
                            "column": 0,
                            "sticky": ctk.W,
                            "padx": 12 + self.left_padding,
                        },
                    }
                )
            else:
                row = check_row

        for widget in widgets:
            widget["widget"].grid(**widget["grid_args"])

    def init(self):
        for key, var in self.chosen_options.items():
            var.set(self.default_options[key])
        self.is_all.set(False)
        self._callback()

    def _all_options(self):
        if self.is_all.get():
            for v in self.chosen_options.values():
                v.set(True)
        else:
            for v in self.chosen_options.values():
                v.set(False)
        self._callback()

    def _select_checkbox(self):
        if all(v.get() for v in self.chosen_options.values()):
            self.is_all.set(True)
        else:
            self.is_all.set(False)

        self._callback()

    def _callback(self):
        result = {k: v.get() for k, v in self.chosen_options.items()}
        self.on_check(result)
