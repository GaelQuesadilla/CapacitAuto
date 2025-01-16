import tkinter as tk
import ttkbootstrap as ttk
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton


class HomeView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)
        self.header = ttk.Frame(self)
        self.header.pack(fill=ttk.X)

        self.title = TitleLabel(self.header, text="Bienvenido")
        self.title.pack(side=ttk.LEFT)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = HomeView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
