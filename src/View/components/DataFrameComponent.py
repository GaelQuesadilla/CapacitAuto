import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from src.Log import setup_logger
import os
from src.View.components.BaseView import BaseView

logger = setup_logger(loggerName="DataFrameComponent")


class DataFrameComponent(tk.Frame):
    def __init__(self, parent: tk.Tk, df: pd.DataFrame = None, fileName: str = None):
        super().__init__(parent)
        self._pd = df
        self._parent = parent
        self._tree: ttk.Treeview = None
        self.fileName = fileName

        if self.pd is None:
            self.loadDataFrame()

        self._createComponent()

    def _createComponent(self):
        columns = list(self.pd.columns)
        self._tree = ttk.Treeview(self, columns=columns, show="headings")

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center")

        for _, row in self.pd.iterrows():
            self.tree.insert("", "end", values=row.tolist())

        v_scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(
            self, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=v_scrollbar.set,
                            xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        h_scrollbar.grid(row=1, column=0, sticky=tk.EW)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def loadDataFrame(self):
        if self.fileName is None:
            error = "No se ha proporcionado ningún archivo para acceder."
            logger.error(error)
            raise ValueError(error)

        if not os.path.isfile(self.fileName):
            error = f"No es posible acceder al archivo {self.fileName}."
            logger.error(error)
            self._pd = pd.DataFrame()
            messagebox.showwarning(
                "Atención",
                f"No es posible acceder al archivo {
                    self.fileName}.\nPor favor, inserte el archivo"
            )

            return

        self._pd = pd.read_excel(self.fileName)

    @property
    def pd(self):
        return self._pd

    @property
    def tree(self):
        return self._tree


if __name__ == "__main__":
    from src.Config import Config

    fileName = os.path.join(
        Config.read("Files", "data_dir"),
        "lists\\TEST\\Lista Alumnos 2-A.xlsx"
    )
    base = BaseView()
    component = DataFrameComponent(base.root, fileName=fileName)
    component.pack(fill=tk.BOTH, expand=True)

    base.show()
