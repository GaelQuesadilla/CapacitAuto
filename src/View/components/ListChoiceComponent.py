import tkinter as tk
from tkinter import ttk
from typing import List
import pathlib
from src.Config import Config


class MultipleListComponent(tk.Frame):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        self.listDir: pathlib.Path = Config.getPath("Files", "lists_dir")
        self.files: List[pathlib.Path] = []
        self.files: List[pathlib.Path] = []

        self.parent: tk.Tk = parent
        self.frame: tk.Frame = tk.Frame(
            self.parent,
            padx=5,
            pady=10
        )
        self.selector: ttk.Combobox = None

        self.getFiles()
        self._createComponent()

    def getFiles(self):
        paths = self.listDir.glob("*")
        self.files = [x for x in paths if x.is_file()]
        self.fileNames = [x.name for x in self.files]

        return self.files

    def _createComponent(self):
        self.selector = ttk.Combobox(
            self.frame,
            values=self.fileNames,
            width=30
        )

        self.frame.pack()
        self.selector.pack(expand=True)

    @property
    def value(self):
        return self.selector.get()


if __name__ == "__main__":
    from src.View.components.BaseView import BaseView
    base = BaseView()

    component = MultipleListComponent(base.root)
    component.pack()

    base.show()
