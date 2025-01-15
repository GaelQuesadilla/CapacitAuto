import tkinter as tk
from src.View.widgets.StudentsListWidget import StudentsListWidget
from src.View.widgets.ListChoiceWidget import ListChoiceWidget
from src.View.widgets.TopWindow import TopWindow
import pathlib
from src.Config import Config
import pandas as pd
from src.View.widgets.ProgressTask import ProgressTask
import json
from tkinter import ttk
from src.Log import setup_logger
from src.Model.models.AdvancedGroup import AdvancedGroup
from src.Model.models.StudentList import StudentList
from typing import List
from tkinter import messagebox

logger = setup_logger(loggerName=__name__)


class ResultsView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.kardexData = json.load(Config.getPath(
            "Files", "kardex_data_dir").open()
        )

        self.title = tk.Label(self, text="Listas de alumnos")
        self.title.pack(fill=tk.X)

        self.calcResultsButton = tk.Button(
            self, text="Calcular grupos", command=self.calcResults
        )
        self.calcResultsButton.pack()

        self.instruction = tk.Label(
            self, text="Selecciona la lista para verla")
        self.instruction.pack()

        self.listsCombobox = ListChoiceWidget(
            self, Config.getPath("Files", "list_results_dir")
        )
        self.listsCombobox.bind('<<ComboboxSelected>>', self.setList)
        self.listsCombobox.pack()

        if not self.path:
            self.list = StudentsListWidget(
                self, df=pd.DataFrame())
        else:
            self.list = StudentsListWidget(
                self, fileName=self.path)

        self.list.pack(fill=tk.BOTH, expand=True)

    def setList(self, event):
        self.list.fileName = self.path
        self.list.loadDataFrame()
        self.list._createComponent()

    def calcResults(self):
        self.getSemester(self._processResults)

    def getSemester(self, callback):
        """Abre un TopWindow para seleccionar el semestre y ejecuta un callback al obtenerlo."""
        topWindow = TopWindow(self.master)

        def onSemesterSelected():
            semester = combobox.get()
            if not semester:
                tk.messagebox.showerror(
                    "Error", "Debe seleccionar un semestre.")
                return
            topWindow.destroy()
            callback(semester)

        instructions = tk.Label(
            topWindow, text="Selecciona el semestre a obtener")
        instructions.pack()

        availableSemesters = self.kardexData.get("availableSemesters", [])
        combobox = ttk.Combobox(topWindow, values=availableSemesters)
        combobox.pack()

        confirm_button = tk.Button(
            topWindow, text="Confirmar",
            command=onSemesterSelected
        )
        confirm_button.pack()

    def _processResults(self, semester):
        listNameFormat = Config.read("General", "list_path_format")
        self.kardexData = json.load(Config.getPath(
            "Files", "kardex_data_dir").open()
        )
        shift = Config.read("School", "school_shift")

        @ProgressTask(parent=self.master, title="Calculando grupos")
        def task():
            logger.info(f"Procesando el semestre {semester}")

            availableLists: List[StudentList] = []
            choicesList = pd.read_excel(Config.getPath("Files", "choices_dir"))
            listsDir: pathlib.Path = Config.getPath("Files", "lists_dir")

            for group in self.kardexData.get("availableGroups", []):
                fileName = listNameFormat.format(
                    semestre=semester,
                    grupo=group,
                    turno=shift
                )
                path: pathlib.Path = listsDir / fileName
                if path.is_file():
                    studentList = StudentList(
                        fileName=path,
                        semester=semester,
                        group=group,
                    )

                    logger.info(f"Cargando lista {path}")
                    studentList.load()

                    availableLists.append(studentList)

            advancedGroup = AdvancedGroup(
                semester,
                choicesList,
                * availableLists
            )

            advancedGroup.setPerfectLists()
            try:
                advancedGroup.iterate()
                logger.info("Guardando listas de los grupos calculados")

                resultsDir = Config.getPath("Files", "list_results_dir")
                print(f"{resultsDir=}")

                for course, studentList in advancedGroup.studentLists.items():
                    studentList.fileName = resultsDir / \
                        f"Lista - {course}.xlsx"

                    studentList.sort(by="Nombre")
                    studentList.save()
                    self.listsCombobox.getFiles()
                    self.setList(None)
            except RecursionError:
                messagebox.showwarning(
                    "Advertencia",
                    "No ha sido posible resolver los grupos en multiples iteraciones.\n"
                    "Se recomienda revisar los registros."
                )

        task()

    @ property
    def path(self):
        if self.listsCombobox.get() == "":
            return False

        path = Config.getPath("Files", "list_results_dir") / \
            self.listsCombobox.get()
        return path


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = ResultsView(window)
    view.pack(fill=tk.BOTH, expand=True)

    window.mainloop()
