from typing import Callable
import customtkinter as ctk


class ClearButton(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_click: Callable,
        bg_color: str = "#F2F2F2",
    ):
        super().__init__(parent, fg_color=bg_color)
        self.on_click = on_click

        self.columnconfigure(0, weight=0)
        button = ctk.CTkButton(
            self,
            text="Clear",
            command=self.clear_output,
            width=160,
            font=ctk.CTkFont(size=18, weight="normal"),
        )
        button.grid(row=0, column=0, pady=(0, 4), ipady=8, sticky=ctk.E)

    def clear_output(self):
        self.on_click()
