import pandas as pd
from src.Config import Config
from src.Kardex.AllKardex import getAllKardex
import os
from alive_progress import alive_bar
from src.FileManager.SafeFileName import safeFileName
from src.Log import setup_logger, trackFunction
from .Student import Student

logging = setup_logger()


def setRelevantGrades(student: Student, relevantGrades: dict, courses: list):
    prefix = Config.read("General", "relevant_grades_name")

    for course in courses:
        relevantAverageKey = prefix.format(course)
        student.setExtras(
            relevantAverageKey,
            relevantGrades.get(relevantAverageKey)
        )


@trackFunction
def createStudentsList(allKardexFileDir: str = None):
    """Sorts students according to their semester and group, and then saves them in an Excel file

    Parameters
    ----------
    allKardexFileDir : str, optional
        The path of the Kardex file to get, by default None
    """

    students = getAllKardex(allKardexFileDir)
    logging.info(f"Creando listas de estudiantes...")

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

            studentInfo: Student = Student(
                CURP=student.get("CURP"),
                Nombre=student.get("Name"),
                Semestre=student.get("Semester"),
                Grupo=student.get("Group"),
                Promedio=student.get("Final_Grade"),
                Turno=student.get("Shift")
            )

            prefix = Config.read("General", "relevant_grades_name")

            relevantGrades = student.get("Relevant_Grades")

            if student.get("Semester") in ["1", "2"]:
                setRelevantGrades(studentInfo, relevantGrades, packages)

            if student.get("Semester") in ["3", "4"]:
                setRelevantGrades(studentInfo, relevantGrades, trainings)

            if student.get("Semester") in ["5", "6"]:
                pass

            groups[semester][group].append(studentInfo.to_dict())

            bar()

    for semesterKey, semester in groups.items():
        for groupKey, group in semester.items():

            shift = Config.read("School", "school_shift")
            fileName = f"Lista Alumnos {semesterKey}-{groupKey}-{shift}.xlsx"
            path = os.path.join(Config.read("Files", "lists_dir"), fileName)

            path = safeFileName(
                f"Guardando lista para el grupo {
                    semesterKey}-{groupKey}-{shift}",
                path
            )

            df = pd.DataFrame(group)
            df = df.sort_values(by=["Nombre", "CURP"], ascending=True)
            df.to_excel(path)


if __name__ == "__main__":
    pass
