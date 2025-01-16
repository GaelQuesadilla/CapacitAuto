import ttkbootstrap as ttk
from ttkbootstrap import constants as c


class TitleLabel(ttk.Label):
    def __init__(self, master, text="", style=c.DEFAULT):
        super().__init__(
            master,
            text=text,
            font=(12),
            padding=[10, 10],
            style=style,
            justify=c.CENTER
        )
