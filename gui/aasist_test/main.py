import customtkinter as ctk
from gui.aasist_test.test_screen import TestScreen


def main():
    ctk.set_default_color_theme("custom_theme.json")
    root = ctk.CTk()
    root.title("AASist Test")
    root.resizable(False, False)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = TestScreen(root)
    app.grid(row=0, column=0, sticky=ctk.NSEW)
    root.mainloop()


if __name__ == "__main__":
    main()
