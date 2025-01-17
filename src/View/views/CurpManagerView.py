import tkinter as tk
from src.View.widgets.CurpManagerWidget import CurpManagerWidget
import ttkbootstrap as ttk
from ttkbootstrap import constants as c
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton

from src.View.views.guides.CurpManagementGuide import CurpManagementGuide
from src.View.widgets.TopWindow import TopWindow


class CurpManagerView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.header = ttk.Frame(self)
        self.header.pack(fill=ttk.X)

        self.title = TitleLabel(self.header, text="Administración de CURPS")
        self.title.pack(side=ttk.LEFT)

        self.help = InfoButton(self.header, command=self.showInfo)
        self.help.pack(side=ttk.RIGHT)

        self.curpManagerWidget = CurpManagerWidget(self)
        self.curpManagerWidget.pack(expand=True, fill=ttk.BOTH)

    def showInfo(self):
        window = TopWindow(
            title="Información de la ventana",
            size=[800, 500])
        info = CurpManagementGuide(window)
        info.pack(fill=ttk.BOTH, expand=True)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = CurpManagerView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
