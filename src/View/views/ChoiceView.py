import ttkbootstrap as ttk
import tkinter as tk
from src.View.widgets.ChoiceWidget import ChoiceWidget
from src.Config import Config
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton
from src.View.widgets.TopWindow import TopWindow
from src.View.views.guides.ChoicesGuide import ChoicesGuide


class ChoiceView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.header = ttk.Frame(self)
        self.header.pack(fill=ttk.X)

        self.title = TitleLabel(self.header, text="Elecciones de los alumnos")
        self.title.pack(side=ttk.LEFT)

        self.help = InfoButton(self.header, command=self.showInfo)
        self.help.pack(side=ttk.RIGHT)
        self.choiceWidget = ChoiceWidget(self)
        self.choiceWidget.pack(expand=True, fill=ttk.BOTH)

    def showInfo(self):

        window = TopWindow(
            title="Información de la ventana",
            size=[800, 500])
        info = ChoicesGuide(window)
        info.pack(fill=ttk.BOTH, expand=True)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = ChoiceView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
