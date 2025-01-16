import tkinter as tk
import ttkbootstrap as ttk
from src.View.widgets.StudentsListWidget import StudentsListWidget
from src.View.widgets.ListChoiceWidget import ListChoiceWidget
import pathlib
import pandas as pd
from src.Config import Config


class ListsView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.title = ttk.Label(self, text="Listas de alumnos")
        self.title.pack(fill=ttk.X)

        self.instruction = ttk.Label(self, text="Selecciona la lista")
        self.instruction.pack()

        self.listsCombobox = ListChoiceWidget(self)
        self.listsCombobox.bind('<<ComboboxSelected>>', self.setList)
        self.listsCombobox.pack()

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
