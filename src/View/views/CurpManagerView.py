import tkinter as tk
from src.View.widgets.CurpManagerWidget import CurpManagerWidget
import ttkbootstrap as ttk


class CurpManagerView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.title = ttk.Label(self, text="Administración de CURPS")
        self.title.pack(fill=ttk.X)
        self.curpManagerWidget = CurpManagerWidget(self)
        self.curpManagerWidget.pack(expand=True, fill=ttk.BOTH)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = CurpManagerView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
