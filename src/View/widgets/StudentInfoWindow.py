from src.View.widgets.TopWindow import TopWindow
import tkinter as tk
from typing import Dict, Union
import ttkbootstrap as ttk


class StudentInfoWindow(TopWindow):

    def __init__(self, parent: tk.Widget, studentKardex: Dict[str, Union[str, int]]):
        super().__init__(parent)
        self.studentKardex = studentKardex
        self.subjectFrame = ttk.Frame()
        self.show()

    def show(self):

        self.title("Información del Estudiante")
        self.geometry("700x500")

        container = ttk.Frame(self)
        container.pack(fill=ttk.BOTH, expand=True)

        canvas = ttk.Canvas(container)
        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=canvas.yview)
        self.scrollableFrame = ttk.Frame(canvas)

        self.scrollableFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        title_label = ttk.Label(
            self.scrollableFrame,
            text="Información del Estudiante",
            padding=[0, 10],
            font=("Arial", 16, "bold")
        )
        title_label.pack(fill=ttk.X)

        basicData = {
            "Nombre": self.studentKardex.get("Name"),
            "CURP": self.studentKardex.get("CURP"),
            "Semestre": self.studentKardex.get("Semester"),
            "Grupo": self.studentKardex.get("Group"),
            "Turno": "Matutino" if self.studentKardex.get("Shift") else "Vespertino",
            "Promedio": self.studentKardex.get("Final_Grade"),
        }
        self.dictToView("Datos básicos", basicData, self.scrollableFrame)

        gradeFrame = ttk.Frame(self.scrollableFrame, padding=[10, 10])
        gradeFrame.pack(fill=ttk.BOTH, expand=True)

        gradeTitleFrame = ttk.Label(
            gradeFrame,
            font=(12),
            text="Calificaciones",
        )
        gradeTitleFrame.pack(fill=ttk.X)

        semesters = list(self.studentKardex.get("Grades").keys())

        selectFrame = ttk.Frame(gradeFrame, padding=[0, 10])
        selectFrame.pack(fill=ttk.X)

        semesterLabel = ttk.Label(
            selectFrame, text="Semestre:", padding=[5, 0])
        semesterLabel.pack(side=ttk.LEFT)

        self.semesterSelector = ttk.Combobox(selectFrame, values=semesters)
        self.semesterSelector.bind("<<ComboboxSelected>>", self.setSubjects)

        self.semesterSelector.pack(side=ttk.LEFT, padx=5)

        # confirmButton = tk.Button(
        #     selectFrame, text="Seleccionar", command=self.setSubjects)
        # confirmButton.pack(side=tk.LEFT, padx=5)

        subjectLabel = ttk.Label(selectFrame, text="Materia:", padding=[5, 0])

        subjectLabel.pack(side=ttk.LEFT)

        self.subjectSelector = ttk.Combobox(selectFrame, values=[])
        self.subjectSelector.bind("<<ComboboxSelected>>", self.showSubject)
        self.subjectSelector.pack(side=ttk.LEFT, padx=5)

        # confirmButton2 = tk.Button(
        #     selectFrame, text="Confirmar", command=self.showSubject)
        # confirmButton2.pack(side=tk.LEFT, padx=5)

    def dictToView(self, title: str, data: Dict[str, Union[str, int]], parent):

        mainFrame = ttk.Frame(parent, padding=[10, 10])
        mainFrame.pack(fill=ttk.X)

        titleLabel = ttk.Label(
            mainFrame,
            font=(10),
            text=title,
        )
        titleLabel.pack(pady=(0, 10), anchor=ttk.W)

        for key, value in data.items():
            value = value if value else "N/A"
            frame = ttk.Frame(mainFrame)
            frame.pack(fill=ttk.X, pady=(0, 5))

            keyLabel = ttk.Label(
                frame,
                text=f"{key}:",
                font=("bold"),
                width=15,
                anchor=ttk.E
            )
            keyLabel.pack(side=ttk.LEFT)

            valueLabel = ttk.Label(
                frame,
                text=value,
                anchor=ttk.W
            )
            valueLabel.pack(side=ttk.LEFT, fill=ttk.X, expand=True)

        return mainFrame

    def setSubjects(self, *args):
        semester = self.semesterSelector.get()
        subjects = [
            subject
            for subject in self.studentKardex.get("Grades").get(semester)
        ]
        self.subjectSelector.config(values=subjects)
        self.subjectSelector.set(value="")

    def showSubject(self, *args):

        self.subjectFrame.destroy()
        semester = self.semesterSelector.get()
        subject = self.subjectSelector.get()
        grades = self.studentKardex.get("Grades").get(semester).get(subject)

        grades = {
            "Primer periodo": grades.get("1"),
            "Segundo periodo": grades.get("2"),
            "Tercer periodo": grades.get("3"),
            "Extra": grades.get("Extra"),
            "Calificación final": grades.get("Final"),
        }

        self.subjectFrame = self.dictToView(
            f"Calificaciones de {subject}", grades, self.scrollableFrame)
