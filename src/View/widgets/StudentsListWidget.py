from src.View.widgets.DataframeWidget import DataframeWidget
from src.View.widgets.AppWindow import AppWindow
import tkinter as tk
from src.Model.services.AllKardex import AllKardex
from src.Config import Config
from src.View.widgets.StudentInfoWindow import StudentInfoWindow


class StudentsListWidget(DataframeWidget):

    def __init__(self, parent, df=None, fileName=None):
        super().__init__(parent, df, fileName)

        self.allKardex = AllKardex(
            fileName=Config.getPath("Files", "all_kardex_dir")
        )
        self.allKardex.loadAllKardex()

    def _createButtons(self):
        super()._createButtons()

        viewStudentButton = tk.Button(
            self.optionFrame, text="Ver información del alumno", command=self.viewStudent
        )

        print("pack viewStudentButton")
        viewStudentButton.pack(side=tk.LEFT, padx=10)

    def viewStudent(self):
        selected = self._tree.focus()

        values = self._tree.item(selected, "values")
        curp = values[0]

        studentKardex = [
            kardex for kardex in self.allKardex.allKardex if kardex.get("CURP") == curp]
        StudentInfoWindow(self.master, studentKardex[0])


if __name__ == "__main__":
    from src.Config import Config

    fileName = Config.getPath("Files", "lists_dir") / \
        "Lista Alumnos 7-D-M.xlsx"
    view = AppWindow()
    component = StudentsListWidget(view, fileName=fileName)
    component.pack(fill=tk.BOTH, expand=True)

    view.mainloop()
