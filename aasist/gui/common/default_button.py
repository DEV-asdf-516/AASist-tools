import customtkinter as ctk
from typing import Callable, Dict


class DefaultButton(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_click: Callable[[Dict[str, bool]], None],
        default_options: Dict[str, bool] = {},
        bg_color: str = "#F2F2F2",
    ):
        super().__init__(parent, fg_color=bg_color)
        self.on_click = on_click
        self.default_options = default_options

        self.columnconfigure(0, weight=0)
        button = ctk.CTkButton(
            self,
            text="Default",
            command=self.reset_options,
            width=120,
            font=ctk.CTkFont(size=14, weight="normal"),
        )
        button.grid(row=0, column=0, padx=8, pady=8, ipady=8, sticky=ctk.W)

    def reset_options(self):
        self.on_click(self.default_options)
