from tkinter import ttk, Tk
from tkinter import messagebox, filedialog
import tkinter as tk
from typing import List, Set, Dict
from src.Log import setup_logger
from src.Config import Config
from src.Model.services.AllKardex import AllKardex
import pathlib
from src.Model.services.CreateStudentList import createStudentsList
from src.View.widgets.ProgressTask import ProgressTask
from src.View.widgets.DataframeWidget import DataframeWidget
import pandas as pd
import json

logger = setup_logger(loggerName=__name__)


class CurpManagerWidget(DataframeWidget):
    def __init__(self, parent):
        self.columns = ["No.", "CURP", "Nombre", "Semestre",  "Estado"]
        self.curpFile: pathlib.Path = Config.getPath("Files", "curps_dir")
        self.kardexDataFile: pathlib.Path = Config.getPath(
            "Files", "kardex_data_dir")
        self.kardexFile: pathlib.Path = Config.getPath(
            "Files", "all_kardex_dir")

        super().__init__(parent, pd.DataFrame())

    def _createComponent(self):

        self._df = self.getDf()

        super()._createComponent()

        self.tree.column(self.columns[0], width=40)
        self.tree.column(self.columns[1], width=200)
        self.tree.column(self.columns[3], width=80)
        self.tree.column(self.columns[4], width=200)

        for row in self.tree.get_children():
            values = self.tree.item(row, "values")
            tags = self.tree.item(row, "tags")
            index, curp, name, semester, status = values

            parityTag = "odd" if int(index) % 2 == 0 else "even"

            if curp in self.requestedCurps:
                pass
            elif curp in self.invalidCurps:
                self.tree.item(row, tags=(f"{parityTag}-error",))
            else:
                self.tree.item(row, tags=(f"{parityTag}-unsolicited",))

        self.tree.tag_configure("error", background="#f2c6de")
        self.tree.tag_configure("unsolicited", background="#faedcb")

        self.tree.tag_configure("even-error", background="#f2c6de")
        self.tree.tag_configure("odd-error", background="#fce3e9")
        self.tree.tag_configure("even-unsolicited", background="#faedcb")
        self.tree.tag_configure("odd-unsolicited", background="#fdf4e3")

    def _createButtons(self):
        super()._createButtons()

        self.loadCurpsFromFileButton = tk.Button(
            self.optionFrame, text="Cargar Curps desde archivo", command=self.loadCurpsFromFile
        )
        self.loadCurpsFromFileButton.pack(side=tk.LEFT, padx=3)

        self.requestKardexButton = tk.Button(
            self.optionFrame, text="Solicitar kardex", command=self.requestKardex
        )
        self.requestKardexButton.pack(side=tk.LEFT, padx=3)

    def loadCurpsFromFile(self):
        newFilePath = filedialog.askopenfilename(
            title="Selecciona el archivo de las CURP",
            initialdir="~",
            filetypes=(("text files", "*.txt"),)
        )

        newFilePath = pathlib.Path(newFilePath)

        if newFilePath.is_file():

            currentCurps = set(self.curps)
            newCurps = set(newFilePath.read_text().splitlines())

            nextCurps = sorted(currentCurps | newCurps)

            with open(self.curpFile, "w") as file:
                for curp in nextCurps:
                    file.write(f"{curp}\n")
        self._createComponent()

    def getDf(self):

        kardex = []
        try:
            kardex: List[str] = json.load(self.kardexFile.open())
        except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
            logger.warning("No es posible obtener el archivo de kardex")

        kardexData: Dict[str] = json.load(self.kardexDataFile.open())

        data = [
            {
                self.columns[0]: i + 1,
                self.columns[1]: curp,
                self.columns[2]: student.get("Name", "SN") if student else "SN",
                self.columns[3]: student.get("Semester", "SN") if student else "SN",
                self.columns[4]: (
                    "Kardex solicitado" if curp in self.requestedCurps else
                    "CURP no valida" if curp in self.invalidCurps else
                    "Kardex no solicitado"
                ),
            }
            for i, curp in enumerate(self.curps)
            for student in (next((s for s in kardex if s.get("CURP") == curp), None),)
        ]
        df = pd.DataFrame(data)

        return df

    def requestKardex(self):

        def onTaskComplete():
            self._createComponent()
            messagebox.showinfo(
                "Se ha completado la solicitud",
                "Se ha solicitado el kardex de todos los alumnos"
            )
            self.showCurpResume()

        @ProgressTask(parent=self.master, title="Solicitando datos...", onComplete=onTaskComplete)
        def task():
            allKardex = AllKardex(fileName=self.kardexFile, curps=self.curps)
            # allKardex.requestAllKardex()
            # allKardex.saveAllKardex()
            # allKardex.saveReport()

            createStudentsList(Config.getPath("Files", "all_kardex_dir"))

        task()

    def showCurpResume(self):
        expectedCurps = Config.read(
            "School", "max_students_in_group") * Config.read("School", "groups") * 3

        message = f"""
        Se cuenta con {len(self.curps)} de {expectedCurps} CURPS
        {len(self.invalidCurps)} CURPS son invalidas
        {len(self.requestedCurps)} CURPS ya han sido solicitadas
        {len(self.curps) - len(self.invalidCurps) - len(self.requestedCurps)} CURPS Están pendientes de solicitar
        """
        messagebox.showinfo("RESUMEN DE SOLICITUD DE CURPS", message)

    @property
    def curps(self):
        return self.curpFile.read_text().splitlines()

    @property
    def requestedCurps(self):

        try:
            kardex: List[str] = json.load(self.kardexFile.open())
            return [student.get("CURP") for student in kardex]
        except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
            return []

    @property
    def invalidCurps(self):
        kardexData: Dict[str] = json.load(self.kardexDataFile.open())
        return kardexData.get("invalidCurps", [])


if __name__ == "__main__":
    from src.Config import Config
    from src.View.widgets.AppWindow import AppWindow

    view = AppWindow()

    component = CurpManagerWidget(view)
    component.pack(fill=tk.BOTH, expand=True)

    view.mainloop()
