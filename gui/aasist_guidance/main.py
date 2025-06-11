import customtkinter as ctk
from build_gui import get_resource_path
from gui.aasist_guidance.guidance_screen import GuidanceScreen


def main():
    theme_path = get_resource_path("custom_theme.json")
    ctk.set_default_color_theme(theme_path)
    root = ctk.CTk()
    root.title("AASist Guidance")
    root.iconbitmap(get_resource_path("icons/guidance.ico"))
    root.resizable(False, False)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = GuidanceScreen(root)
    app.grid(row=0, column=0, sticky=ctk.NSEW)
    root.mainloop()


if __name__ == "__main__":
    main()
