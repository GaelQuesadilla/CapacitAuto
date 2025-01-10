from src.View.widgets.TopWindow import TopWindow
import tkinter as tk
from typing import Dict, Union
from tkinter import ttk


class StudentInfoWindow(TopWindow):

    def __init__(self, parent: tk.Tk, studentKardex: Dict[str, Union[str, int]]):
        super().__init__(parent)
        self.studentKardex = studentKardex
        self.subjectFrame = tk.Frame()
        self.show()

    def show(self):

        self.title("Información del Estudiante")
        self.geometry("700x500")

        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(
            container, orient="vertical", command=canvas.yview)
        self.scrollableFrame = tk.Frame(canvas)

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

        title_label = tk.Label(
            self.scrollableFrame,
            text="Información del Estudiante",
            pady=10,
            font=("Arial", 16, "bold")
        )
        title_label.pack(fill=tk.X)

        basicData = {
            "Nombre": self.studentKardex.get("Name"),
            "CURP": self.studentKardex.get("CURP"),
            "Semestre": self.studentKardex.get("Semester"),
            "Grupo": self.studentKardex.get("Group"),
            "Turno": "Matutino" if self.studentKardex.get("Shift") else "Vespertino",
            "Promedio": self.studentKardex.get("Final_Grade"),
        }
        self.dictToView("Datos básicos", basicData, self.scrollableFrame)

        gradeFrame = tk.Frame(self.scrollableFrame, padx=10,
                              pady=10, relief=tk.RIDGE)
        gradeFrame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        gradeTitleFrame = tk.Label(
            gradeFrame,
            font=(12),
            text="Calificaciones",
        )
        gradeTitleFrame.pack(fill=tk.X)

        semesters = list(self.studentKardex.get("Grades").keys())

        selectFrame = tk.Frame(gradeFrame)
        selectFrame.pack(fill=tk.X, pady=10)

        semesterLabel = tk.Label(selectFrame, text="Semestre:")
        semesterLabel.pack(side=tk.LEFT, padx=5)

        self.semesterSelector = ttk.Combobox(selectFrame, values=semesters)
        self.semesterSelector.bind("<<ComboboxSelected>>", self.setSubjects)

        self.semesterSelector.pack(side=tk.LEFT, padx=5)

        # confirmButton = tk.Button(
        #     selectFrame, text="Seleccionar", command=self.setSubjects)
        # confirmButton.pack(side=tk.LEFT, padx=5)

        subjectLabel = tk.Label(selectFrame, text="Materia:")

        subjectLabel.pack(side=tk.LEFT, padx=5)

        self.subjectSelector = ttk.Combobox(selectFrame, values=[])
        self.subjectSelector.bind("<<ComboboxSelected>>", self.showSubject)
        self.subjectSelector.pack(side=tk.LEFT, padx=5)

        # confirmButton2 = tk.Button(
        #     selectFrame, text="Confirmar", command=self.showSubject)
        # confirmButton2.pack(side=tk.LEFT, padx=5)

    def dictToView(self, title: str, data: Dict[str, Union[str, int]], parent):

        mainFrame = tk.Frame(parent)
        mainFrame.pack(fill=tk.X, padx=10, pady=10)

        titleLabel = tk.Label(
            mainFrame,
            font=(10),
            text=title,
        )
        titleLabel.pack(pady=(0, 10), anchor="w")

        for key, value in data.items():
            value = value if value else "N/A"
            frame = tk.Frame(mainFrame)
            frame.pack(fill=tk.X, pady=(0, 5))

            keyLabel = tk.Label(
                frame,
                text=f"{key}:",
                font=("bold"),
                width=15,
                anchor="e"
            )
            keyLabel.pack(side=tk.LEFT)

            valueLabel = tk.Label(
                frame,
                text=value,
                anchor="w"
            )
            valueLabel.pack(side=tk.LEFT, fill=tk.X, expand=True)

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
