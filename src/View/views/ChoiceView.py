import tkinter as tk
from src.View.widgets.ChoiceWidget import ChoiceWidget
from src.Config import Config


class ChoiceView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.title = tk.Label(self, text="Elecciones de los alumnos")
        self.title.pack(fill=tk.X)
        self.choiceWidget = ChoiceWidget(self)
        self.choiceWidget.pack(expand=True, fill=tk.BOTH)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = ChoiceView(window)
    view.pack(fill=tk.BOTH, expand=True)

    window.mainloop()
