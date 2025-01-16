import ttkbootstrap as ttk
from ttkbootstrap import constants as c
import tkinter as tk
from src.View.widgets.AllSubjectsWidget import AllSubjectsWidget
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton


class AllSubjectsView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.header = ttk.Frame(self)
        self.header.pack(fill=ttk.X)

        self.title = TitleLabel(
            self.header, text="Relación de materias con capacitación/paquete")
        self.title.pack(side=ttk.LEFT)

        self.help = InfoButton(self.header)
        self.help.pack(side=ttk.RIGHT)
        self.allSubjectsWidget = AllSubjectsWidget(self)
        self.allSubjectsWidget.pack(expand=True, fill=ttk.BOTH)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = AllSubjectsView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
