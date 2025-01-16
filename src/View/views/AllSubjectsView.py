import ttkbootstrap as ttk
import tkinter as tk
from src.View.widgets.AllSubjectsWidget import AllSubjectsWidget


class AllSubjectsView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.title = ttk.Label(self, text="Relación de materias")
        self.title.pack(fill=ttk.X)
        self.allSubjectsWidget = AllSubjectsWidget(self)
        self.allSubjectsWidget.pack(expand=True, fill=ttk.BOTH)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = AllSubjectsView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
