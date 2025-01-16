import ttkbootstrap as ttk
import tkinter as tk
from src.View.widgets.ChoiceWidget import ChoiceWidget
from src.Config import Config


class ChoiceView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.title = ttk.Label(self, text="Elecciones de los alumnos")
        self.title.pack(fill=ttk.X)
        self.choiceWidget = ChoiceWidget(self)
        self.choiceWidget.pack(expand=True, fill=ttk.BOTH)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = ChoiceView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
