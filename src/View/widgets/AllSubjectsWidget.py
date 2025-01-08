from src.View.widgets.DataframeWidget import DataframeWidget
from src.View.widgets.AppWindow import AppWindow
import tkinter as tk
from tkinter import ttk
from src.Model.services.AllSubjects import AllSubjects
from src.Config import Config
from src.Log import setup_logger
from src.Model.services.CalcRelevantGrades import calcRelevantGrades


from src.View.widgets.ProgressTask import ProgressTask
logger = setup_logger(loggerName=__name__)


class AllSubjectsWidget(DataframeWidget):

    def __init__(self, parent: tk.Tk):

        allSubjectsFileName = Config.getPath("Files", "all_subjects_dir")

        self.allSubjects = AllSubjects(
            kardexFileName=Config.getPath("Files", "all_kardex_dir"),
            allSubjectsFileName=allSubjectsFileName,
        )

        super().__init__(parent=parent, fileName=allSubjectsFileName)

    def _createButtons(self):
        super()._createButtons()

        genButton = tk.Button(
            self.optionFrame, text="Generar archivo", command=self.generateNewSubjectsExcel
        )

        genButton.pack(side=tk.LEFT, padx=10)

    def generateNewSubjectsExcel(self):
        self.allSubjects.getAll()
        self.allSubjects.saveToExcel()

        self.onUpdateDf()
        self._createComponent()

    def onUpdateDf(self):
        @ProgressTask(parent=self.master, title="Calculando promedios relevantes")
        def task():
            calcRelevantGrades()

        task()


if __name__ == "__main__":

    view = AppWindow()
    component = AllSubjectsWidget(view)
    component.pack(fill=tk.BOTH, expand=True)

    view.mainloop()
