import tkinter as tk
import ttkbootstrap as ttk
from src.View.widgets.StudentsListWidget import StudentsListWidget
from src.View.widgets.ListChoiceWidget import ListChoiceWidget
from src.View.widgets.TopWindow import TopWindow
import pathlib
from src.Config import Config
import pandas as pd
from src.View.widgets.ProgressTask import ProgressTask
import json
from src.Log import setup_logger
from src.Model.models.AdvancedGroup import AdvancedGroup
from src.Model.models.StudentList import StudentList
from typing import List
from ttkbootstrap.dialogs.dialogs import Messagebox
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton


logger = setup_logger(loggerName=__name__)


class ResultsView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.kardexData = json.load(Config.getPath(
            "Files", "kardex_data_dir").open()
        )
        # Header
        self.header = ttk.Frame(self)
        self.header.pack(fill=ttk.X)

        self.title = TitleLabel(self.header, text="Nuevos grupos")
        self.title.pack(side=ttk.LEFT)

        self.help = InfoButton(self.header)
        self.help.pack(side=ttk.RIGHT)

        self.calcResultsButton = ttk.Button(
            self.header, text="Calcular grupos", command=self.calcResults
        )
        self.calcResultsButton.pack(side=ttk.RIGHT)

        # Instructions
        self.instructionFrame = ttk.Frame(self)
        self.instructionFrame.pack(fill=ttk.X)

        self.instruction = ttk.Label(
            self.instructionFrame, text="Selecciona la lista a consultar:", padding=[5, 5])
        self.instruction.pack(side=ttk.LEFT)

        self.listsCombobox = ListChoiceWidget(
            self.instructionFrame, Config.getPath("Files", "list_results_dir")
        )
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

    def calcResults(self):
        self.getSemester(self._processResults)

    def getSemester(self, callback):
        """Abre un TopWindow para seleccionar el semestre y ejecuta un callback al obtenerlo."""
        topWindow = TopWindow(self.master)
        frame = ttk.Frame(topWindow)
        frame.pack(expand=True)

        def onSemesterSelected():
            semester = combobox.get()
            if not semester:
                Messagebox.show_error(
                    title="Error",
                    message="Debe seleccionar un semestre.",
                    alert=True
                )
                return
            topWindow.destroy()
            callback(semester)

        instructions = ttk.Label(
            frame, text="Selecciona el semestre a obtener")
        instructions.pack(pady=5)

        availableSemesters = self.kardexData.get("availableSemesters", [])
        combobox = ttk.Combobox(frame, values=availableSemesters)
        combobox.pack(pady=5)
        confirm_button = ttk.Button(
            frame, text="Confirmar",
            command=onSemesterSelected
        )
        confirm_button.pack(pady=5)

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
                Messagebox.show_warning(
                    title="Advertencia",
                    message="No ha sido posible resolver los grupos en multiples iteraciones.\n"
                    "Se recomienda revisar los registros.",
                    alert=True
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
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
