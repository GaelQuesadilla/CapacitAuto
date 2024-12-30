from src.View.components.DataFrameComponent import DataFrameComponent
from src.View.components.BaseView import BaseView
import tkinter as tk
from src.Model.services.AllKardex import AllKardex
from src.Config import Config
from src.View.views.StudentInfoView import StudentInfoView


class StudentsDataFrame(DataFrameComponent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        StudentInfoView(self._parent, studentKardex[0]).show()


if __name__ == "__main__":
    from src.Config import Config

    fileName = Config.getPath("Files", "lists_dir") / \
        "Lista Alumnos 7-D-M.xlsx"
    base = BaseView()
    component = StudentsDataFrame(base.root, fileName=fileName)
    component.pack(fill=tk.BOTH, expand=True)

    base.show()
