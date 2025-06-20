import os
import customtkinter as ctk
from tkinter import filedialog
from typing import Callable, Iterable, List


class FileSelector(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        on_files_selected: Callable[[List[str]], None],
        file_types: Iterable = None,
        bg_color: str = "#F2F2F2",
    ):
        super().__init__(parent, fg_color=bg_color)

        self.on_selected = on_files_selected
        self.file_types = file_types if file_types else [("AAS", "*.aasx")]
        self.file_paths = []

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        browse_button = ctk.CTkButton(
            self,
            text="Browse",
            command=self.browse_files,
            width=120,
            font=ctk.CTkFont(size=14, weight="normal"),
        )
        browse_button.grid(row=0, column=0, padx=8, pady=8, ipady=8, sticky=ctk.W)

        self.file_display = ctk.CTkTextbox(
            self,
            height=40,
            wrap="none",
            state=ctk.DISABLED,
            font=ctk.CTkFont(size=16, weight="normal"),
        )

        self.file_display._textbox.configure(
            padx=8,
            pady=8,
        )
        self.file_display._textbox.tag_configure("align_left", justify="left")
        self.file_display._textbox.tag_add("align_left", "1.0", "end")

        self.file_display.grid(row=0, column=1, sticky=ctk.EW, padx=8)
        self.file_display.configure(state=ctk.NORMAL)
        self.file_display.delete("1.0", ctk.END)
        self.file_display.configure(text_color="gray")
        self.file_display.insert("1.0", "Select AASX files...")
        self.file_display.configure(state=ctk.DISABLED)

    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Load AASX File", filetypes=self.file_types, defaultextension=".aasx"
        )
        self.file_display.configure(state=ctk.NORMAL)
        if files:
            self.file_paths = list(files)
            display_text = ", ".join([os.path.basename(f) for f in files])
            self.file_display.configure(text_color="black")
            self.file_display.delete("1.0", ctk.END)
            self.file_display.insert("1.0", display_text)
            self.on_selected(self.file_paths)
        else:
            self.file_display.delete("1.0", ctk.END)
            self.file_display.configure(text_color="gray")
            self.file_display.insert("1.0", "Select AASX files...")

        self.file_display.configure(state=ctk.DISABLED)
