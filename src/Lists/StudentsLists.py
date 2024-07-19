import pandas as pd
from src.Config import Config
from src.Kardex.AllKardex import getAllKardex
import os
from alive_progress import alive_bar
from colorama import init, Fore
import pprint
from src.FileManager.SafeFileName import safeFileName
init(autoreset=True)


def createStudentsList():
    """Sorts students according to their semester and group, and then saves them in an Excel file"""

    students = getAllKardex()
    print(f"{Fore.BLUE}Creating Students Lists...")

    packages = Config.read("School", "packages").split(",")
    trainings = Config.read("School", "trainings").split(",")

    groups = {}

    with alive_bar(len(students)) as bar:
        for student in students:
            semester = student.get("Semester")
            group = student.get("Group")

            if groups.get(semester) is None:
                groups[semester] = {}
            if groups.get(semester).get(group) is None:
                groups[semester][group] = []

            studentDataToSave = {
                "CURP": student.get("CURP"),
                "Semestre": student.get("Semester"),
                "Grupo": student.get("Group"),
                "Turno": student.get("Shift"),
                "Nombre": student.get("Name"),
                "Promedio": student.get("Final_Grade"),
            }

            prefix = Config.read("General", "relevant_grades_name")

            if student.get("Semester") in ["1", "2"]:
                for package in packages:
                    relevantAverageKey = prefix.format(package)
                    studentDataToSave[relevantAverageKey] = student.get(
                        "Relevant_Grades").get(relevantAverageKey)

            if student.get("Semester") in ["3", "4"]:
                for training in trainings:
                    relevantAverageKey = prefix.format(training)
                    studentDataToSave[relevantAverageKey] = student.get(
                        "Relevant_Grades").get(relevantAverageKey)

            if student.get("Semester") in ["5", "6"]:
                pass

            groups[semester][group].append(studentDataToSave)

            bar()

    for semesterKey, semester in groups.items():
        for groupKey, group in semester.items():

            shift = Config.read("School", "school_shift")
            fileName = f"Lista Alumnos {semesterKey}-{groupKey}-{shift}.xlsx"
            path = os.path.join(Config.read("Files", "lists_dir"), fileName)

            path = safeFileName(path)

            df = pd.DataFrame(group)
            df = df.sort_values(by=["Nombre", "CURP"], ascending=True)
            df.to_excel(path)


if __name__ == "__main__":
    pass
