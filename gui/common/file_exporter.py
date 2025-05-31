import customtkinter as ctk
from typing import Callable


class FileExporter(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        on_export: Callable,
        bg_color: str = "#F2F2F2",
        **kwargs
    ):
        super().__init__(parent, fg_color=bg_color)

        self.on_export = on_export

        export_button = ctk.CTkButton(
            self,
            text="Export",
            command=lambda: self.export_files(**kwargs),
            width=160,
            font=ctk.CTkFont(size=18, weight="normal"),
        )
        export_button.grid(row=0, column=0, pady=(0, 4), ipady=8, sticky=ctk.E)

    def export_files(self, **kwargs: any):
        self.on_export(**kwargs)
