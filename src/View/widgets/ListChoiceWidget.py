import tkinter as tk
from tkinter import ttk
from typing import List
import pathlib
from src.Config import Config
from src.Log import setup_logger

logger = setup_logger()


class ListChoiceWidget(ttk.Combobox):
    def __init__(
        self, parent: tk.Tk,
        listDir: pathlib.Path = Config.getPath("Files", "lists_dir")
    ):
        super().__init__(parent)

        self.listDir = listDir
        self.files: List[pathlib.Path] = []
        self.files: List[pathlib.Path] = []

        self.parent: tk.Tk = parent

        self.getFiles()

        self.config(values=self.fileNames, width=30)

    def getFiles(self):
        paths = self.listDir.glob("*")
        self.files = [x for x in paths if x.is_file()]
        self.fileNames = [x.name for x in self.files]
        self.set(value="")
        try:
            self.config(values=self.fileNames)
            self.set(self.fileNames[0])
        except IndexError as e:
            logger.warning(f"No se encuentra ningún archivo en {self.listDir}")


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow
    view = AppWindow()

    component = ListChoiceWidget(view)
    component.pack()

    view.mainloop()
