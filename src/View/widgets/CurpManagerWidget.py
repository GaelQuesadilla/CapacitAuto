from tkinter import ttk, Tk
from tkinter import messagebox, filedialog
import tkinter as tk
from typing import List, Set, Dict
import os
from src.Log import setup_logger
from src.Config import Config
from src.Model.services.AllKardex import AllKardex
import pathlib
from src.View.widgets.ProgressTask import ProgressTask
from src.View.widgets.DataframeWidget import DataframeWidget
import pandas as pd
import json

logger = setup_logger(loggerName="src.View.views.CurpManagerView")


class CurpManagerWidget(DataframeWidget):
    def __init__(self, parent):
        self.columns = ["No.", "CURP", "Estado"]
        self.curpFile: pathlib.Path = Config.getPath("Files", "curps_dir")
        self.kardexDataFile: pathlib.Path = Config.getPath(
            "Files", "kardex_data_dir")
        self.kardexFile: pathlib.Path = Config.getPath(
            "Files", "all_kardex_dir")

        super().__init__(parent, self.df)

    @property
    def df(self):

        data = [
            {
                self.columns[0]: i+1,
                self.columns[1]: curp,
                self.columns[2]: (
                    "Kardex solicitado" if curp in self.requestedCurps else
                    "CURP no valida" if curp in self.invalidCurps else
                    "Kardex no solicitado"
                ),

            }
            for i, curp in enumerate(self.curps)
        ]
        df = pd.DataFrame(data)

        return df

    @property
    def curps(self):
        return self.curpFile.read_text().splitlines()

    @property
    def requestedCurps(self):
        kardex: List[str] = json.load(self.kardexFile.open())

        return [student.get("CURP") for student in kardex]

    @property
    def invalidCurps(self):
        kardexData: Dict[str] = json.load(self.kardexDataFile.open())
        return kardexData.get("invalidCurps", [])


class CURPManagerView():
    def __init__(self, parent):
        self.parent = parent
        self.curpsFile = Config.read("Files", "curps_dir")
        self.curps: List[str] = None
        self.invalidCurps: List[str] = None
        self.solicitedCurps: List[str] = None
        self.encoding = Config.read("General", "encoding")
        self.status = {
            "unsolicited": "No solicitado",
            "solicited": "Solicitado",
            "error": "CURP invalida",
        }

        self.reportDir = Config.read("Files", "curp_report_dir")

        self.allKardexDir = Config.read("Files", "all_kardex_dir")

    def getCurps(self):

        curps = Config.getPath("Files", "curps_dir").read_text().splitlines()
        self.curps: Set[str] = set(curps)

        invalidCurps = open(
            self.reportDir, "r", encoding=self.encoding
        ).read()
        self.invalidCurps: Set[str] = set(invalidCurps.splitlines())

        self.solicitedCurps: Set[str] = set()
        try:
            allKardex = AllKardex(fileName=self.allKardexDir)

            allKardex.loadAllKardex()

            self.solicitedCurps = set([
                student.get("CURP")
                for student in allKardex.allKardex
            ])
        except:
            pass

    def clearTree(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

    def showCurps(self):
        self.clearTree()
        curps = list(self.curps)
        curps.sort()
        for i, curp in enumerate(curps):

            status = self.status.get("unsolicited")
            tag = "unsolicited"

            if curp in self.invalidCurps:
                tag = "error"

            if curp in self.solicitedCurps:
                tag = "solicited"

            status = self.status.get(tag)
            self.tree.insert("", tk.END, values=(
                i+1, curp, status), tags=(tag,))

    def loadCurpsFromFile(self):
        newFilePath = filedialog.askopenfilename(
            title="Selecciona el archivo de las CURP",
            initialdir="~",
            filetypes=(("text files", "*.txt"),)
        )

        newFilePath = pathlib.Path(newFilePath)

        if newFilePath.is_file():
            with open(newFilePath, "r") as file:
                curpsFromFile = file.read().splitlines()

            for curp in curpsFromFile:
                self.curps.add(curp)
            with open(self.curpsFile, "w") as file:
                for curp in self.curps:
                    file.write(f"{curp}\n")
        self.showCurps()

    def requestKardex(self):

        def onTaskComplete():
            self.getCurps()
            self.showCurps()
            messagebox.showinfo(
                "Se ha completado la solicitud",
                "Se ha solicitado el kardex de todos los alumnos"
            )
            self.showCurpResume()

        @ProgressTask(parent=self.parent, title="Solicitando datos...", onComplete=onTaskComplete)
        def task():
            allKardex = AllKardex(fileName=self.allKardexDir, curps=self.curps)
            allKardex.requestAllKardex()
            allKardex.saveAllKardex()
            allKardex.saveReport()

        task()

    def showCurpResume(self):
        expectedCurps = Config.read(
            "School", "max_students_in_group") * Config.read("School", "groups") * 3

        message = f"""
        Se cuenta con {len(self.curps)} de {expectedCurps} CURPS
        {len(self.invalidCurps)} CURPS son invalidas
        {len(self.solicitedCurps)} CURPS ya han sido solicitadas
        {len(self.curps) - len(self.invalidCurps) - len(self.solicitedCurps)} CURPS Están pendientes de solicitar
        """
        messagebox.showinfo("RESUMEN DE SOLICITUD DE CURPS", message)

    def show(self):
        self.window = tk.Toplevel(self.parent)
        self.window.geometry("600x400")

        self.tree = ttk.Treeview(
            self.window, columns=("INDEX", "CURP", "STATUS"), show="headings", height=15)

        self.tree.heading("INDEX", text="No.")
        self.tree.heading("CURP", text="CURP")
        self.tree.heading("STATUS", text="ESTADO")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.getCurps()
        self.showCurps()

        self.actionButtonFrame = tk.Frame(self.window)
        self.actionButtonFrame.pack(fill=tk.X, pady=10)

        self.loadCurpsFromFileButton = tk.Button(
            self.actionButtonFrame, text="Cargar Curps desde archivo", command=self.loadCurpsFromFile)
        self.loadCurpsFromFileButton.pack(side=tk.LEFT, padx=3)

        self.requestKardexButton = tk.Button(
            self.actionButtonFrame, text="Solicitar CURPS", command=self.requestKardex)
        self.requestKardexButton.pack(side=tk.LEFT, padx=3)

        self.showCurpResumeButton = tk.Button(
            self.actionButtonFrame, text="Mostrar resumen", command=self.showCurpResume)
        self.showCurpResumeButton.pack(side=tk.LEFT, padx=3)

        self.tree.tag_configure(
            "error", background="#fdaaaa"
        )
        self.tree.tag_configure(
            "unsolicited"
        )
        self.tree.tag_configure(
            "solicited", background="#ddf1da"
        )


if __name__ == "__main__":
    from src.Config import Config
    from src.View.widgets.AppWindow import AppWindow

    view = AppWindow()

    component = CurpManagerWidget(view)
    component.pack(fill=tk.BOTH, expand=True)

    view.mainloop()
