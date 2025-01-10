import pandas as pd
from src.Config import Config
from src.Model.services.AllKardex import AllKardex
import os
from src.Log import setup_logger, trackFunction
from src.Model.models.StudentList import StudentList
from src.Model.models.Student import Student
import pathlib

logging = setup_logger()


def setRelevantGrades(student: Student, relevantGrades: dict, courses: list):
    prefix = Config.read("General", "relevant_grades_name")

    for course in courses:
        relevantAverageKey = prefix.format(course)
        student.setExtras(
            **{
                relevantAverageKey: relevantGrades.get(relevantAverageKey)
            }
        )


@trackFunction
def createStudentsList(allKardexFileDir: str = None):
    """Sorts students according to their semester and group, and then saves them in an Excel file

    Parameters
    ----------
    allKardexFileDir : str, optional
        The path of the Kardex file to get, by default None
    """
    allKardex = AllKardex(fileName=allKardexFileDir)
    allKardex.loadAllKardex()
    students = allKardex.allKardex
    logging.info(f"Creando listas de estudiantes...")

    packages = Config.read("School", "packages").split(",")
    trainings = Config.read("School", "trainings").split(",")

    groups = {}

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

        groups[semester][group].append(studentInfo)

    for semesterKey, semester in groups.items():
        for groupKey, group in semester.items():

            shift = Config.read("School", "school_shift")

            fileName = Config.read("General", "list_path_format").format(
                semestre=semesterKey,
                grupo=groupKey,
                turno=shift
            )
            path = Config.getPath("Files", "lists_dir") / fileName

            studentList = StudentList(
                fileName=path,
                semester=semesterKey,
                group=groupKey
            )

            for student in group:
                studentList.addStudent(student)

            studentList.sort(by=["Nombre", "CURP"], ascending=True)
            choicePrefix = Config.read("General", "choice_name").format("")

            columnsToDrop = [
                col for col in studentList.df.columns if choicePrefix in str(col)
            ]

            studentList.df.drop(columns=columnsToDrop, inplace=True)
            studentList.save()


if __name__ == "__main__":

    createStudentsList(Config.read("Files", "all_kardex_dir"))
