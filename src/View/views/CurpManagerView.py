import tkinter as tk
from src.View.widgets.CurpManagerWidget import CurpManagerWidget


class CurpManagerView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.title = tk.Label(self, text="Administración de CURPS")
        self.title.pack(fill=tk.X)
        self.curpManagerWidget = CurpManagerWidget(self)
        self.curpManagerWidget.pack(expand=True, fill=tk.BOTH)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = CurpManagerView(window)
    view.pack(fill=tk.BOTH, expand=True)

    window.mainloop()
