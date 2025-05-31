import customtkinter as ctk


class TestScreen(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(parent)
        self.parent = parent
        self.theme_data = ctk.ThemeManager.theme
        self.layout()

    def layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
