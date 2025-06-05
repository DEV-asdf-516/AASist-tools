import threading
import customtkinter as ctk
from typing import Any, Callable


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
        self.stop_event = threading.Event()
        self.is_processing = False

        export_button = ctk.CTkButton(
            self,
            text="Export",
            command=lambda: self.start(**kwargs),
            width=160,
            font=ctk.CTkFont(size=18, weight="normal"),
        )
        export_button.grid(row=0, column=0, pady=(0, 4), ipady=8, sticky=ctk.E)

    def export_files(self, **kwargs: any):
        self.on_export(**kwargs)
        self.is_processing = False

    def start(self, **kwargs: Any):
        if self.is_processing:
            return
        self.is_processing = True
        self.stop_event.clear()
        self.thread = threading.Thread(
            target=self.export_files, args=(kwargs), daemon=True
        )
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.is_processing = False
