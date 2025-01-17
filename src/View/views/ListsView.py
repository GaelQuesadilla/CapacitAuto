from src.View.widgets.TopWindow import TopWindow
from src.View.views.guides.ListsGuide import ListsGuide
import tkinter as tk
import ttkbootstrap as ttk
from src.View.widgets.StudentsListWidget import StudentsListWidget
from src.View.widgets.ListChoiceWidget import ListChoiceWidget
import pathlib
import pandas as pd
from src.Config import Config
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton
from ttkbootstrap import constants as c


class ListsView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        # Header
        self.header = ttk.Frame(self)
        self.header.pack(fill=ttk.X)

        self.title = TitleLabel(self.header, text="Listas de alumnos")
        self.title.pack(side=ttk.LEFT)

        self.help = InfoButton(self.header, command=self.showInfo)
        self.help.pack(side=ttk.RIGHT)

        # Instructions
        self.instructionFrame = ttk.Frame(self)
        self.instructionFrame.pack(fill=ttk.X)

        self.instruction = ttk.Label(
            self.instructionFrame, text="Selecciona la lista a consultar:", padding=[5, 5])
        self.instruction.pack(side=ttk.LEFT)

        self.listsCombobox = ListChoiceWidget(self.instructionFrame)
        self.listsCombobox.bind('<<ComboboxSelected>>', self.setList)
        self.listsCombobox.pack(side=ttk.LEFT)

        if not self.path:
            self.list = StudentsListWidget(
                self, df=pd.DataFrame())
        else:
            self.list = StudentsListWidget(
                self, fileName=self.path)

        self.list.pack(fill=ttk.BOTH, expand=True)

    def setList(self, event):
        self.list.fileName = self.path
        self.list.loadDataFrame()
        self.list._createComponent()

    def showInfo(self):

        window = TopWindow(
            title="Información de la ventana",
            size=[800, 500])
        info = ListsGuide(window)
        info.pack(fill=ttk.BOTH, expand=True)

    @property
    def path(self):
        print(f"{self.listsCombobox.get()=}")
        if self.listsCombobox.get() == "":
            return False

        path = Config.getPath("Files", "lists_dir") / \
            pathlib.Path(self.listsCombobox.get())
        return path


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = ListsView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
