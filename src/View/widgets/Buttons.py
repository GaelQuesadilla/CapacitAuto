from ttkbootstrap import constants as c
import ttkbootstrap as ttk
from typing import Callable


class InfoButton(ttk.Button):
    def __init__(self, master, command: Callable = None):
        super().__init__(
            master,
            command=command,
            style=c.INFO,
            text="?",
            padding=[10, 5]
        )

        self.pack(padx=5, pady=5)
