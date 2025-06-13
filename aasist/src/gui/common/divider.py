import customtkinter as ctk


class Divider(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        orientation: str = "horizontal",
        thickness: int = 1,
        color: str = "#C9C9C9",
        margin: tuple = (0, 4),  # (x_margin, y_margin)
    ):
        super().__init__(parent, fg_color=color)

        self.orientation = orientation
        self.thickness = thickness
        self.margin = margin
        if orientation == "horizontal":
            self.configure(height=thickness)
        else:
            self.configure(width=thickness)

    def grid_horizontal(self, row: int, column: int = 0, columnspan: int = 1, **kwargs):
        """가로 구분선을 grid로 배치"""
        default_kwargs = {
            "sticky": ctk.EW,
            "padx": self.margin[0],
            "pady": self.margin[1],
        }
        default_kwargs.update(kwargs)
        self.grid(row=row, column=column, columnspan=columnspan, **default_kwargs)

    def grid_vertical(self, column: int, row: int = 0, rowspan: int = 1, **kwargs):
        """세로 구분선을 grid로 배치"""
        default_kwargs = {
            "sticky": ctk.NS,
            "padx": self.margin[0],
            "pady": self.margin[1],
        }
        default_kwargs.update(kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, **default_kwargs)
