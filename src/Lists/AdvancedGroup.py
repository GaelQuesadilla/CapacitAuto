from src.Lists.Group import Group
from src.Lists.Student import Student
from src.Lists.StudentList import StudentList
from typing import List, Dict, Any
from dataclasses import dataclass
import pandas as pd
from src.Config import Config
from src.Log import Log, PrintLog

maxStudents: int = Config.read("School", "max_students_in_group")
optionPrefix: str = Config.read("General", "choice_name")
relevantGradesPrefix: str = Config.read("General", "relevant_grades_name")


class AdvancedGroup(Group):
    def __init__(self, semester: str, *args: StudentList):
        self.courses: List[str] = []
        self.group: str = None
        self._allStudents: pd.DataFrame = pd.concat(
            [studentList.df for studentList in args], ignore_index=True, sort=False)

        # Get courses for the current semester
        if semester in ["1", "2"]:
            self.courses = Config.read("School", "packages").split(",")
            self.group = "Capacitaciones"
        elif semester in ["3", "4"]:
            self.courses = Config.read("School", "trainings").split(",")
            self.group = "Paquetes"
        else:
            PrintLog.warning(
                "Advanced groups should be used only in 1,2,3,4 semesters"
            )

        groups: Dict[str, StudentList] = {}

        if not self.courses is None:
            for course in self.courses:

                groups[course] = StudentList(
                    fileName=f"Lista - {course}.xlsx", group=course, maxStudents=maxStudents, semester=semester)
            super().__init__(semester, self.group, **groups)
        else:
            super().__init__(semester, self.group)

    @property
    def allStudents(self):
        return self._allStudents

    def setPerfectLists(self):
        for course in self.courses:
            currentList = self._studentLists.get(course)
            studentsData: List[Dict[str, Any]] = self.allStudents.loc[
                self.allStudents[optionPrefix.format(course)] == 1
            ].to_dict(orient="records")

            for studentData in studentsData:
                currentStudent = Student(Semestre=self.semester)
                for key, value in studentData.items():
                    currentStudent.set(key, value)

                currentStudent.Semestre = str(currentStudent.Semestre)
                currentList.addStudent(
                    student=currentStudent)

        self.sortByGrades()

    def sortByGrades(self):
        for course in self.courses:
            currentList = self._studentLists[course]
            currentList.sort(ascending=False, by=[
                             "Promedio", relevantGradesPrefix.format(course)])


if __name__ == "__main__":
    studentListA = StudentList(
        fileName="data\\lists\\TEST\\Lista Alumnos 2-A.xlsx",
        group="A",
        semester="2"
    )
    studentListA.load()

    studentListB = StudentList(
        fileName="data\\lists\\TEST\\Lista Alumnos 2-B.xlsx",
        group="B",
        semester="2"
    )
    studentListB.load()

    studentListC = StudentList(
        fileName="data\\lists\\TEST\\Lista Alumnos 2-C.xlsx",
        group="C",
        semester="2"
    )
    studentListC.load()

    studentListD = StudentList(
        fileName="data\\lists\\TEST\\Lista Alumnos 2-D.xlsx",
        group="D",
        semester="2"
    )
    studentListD.load()

    advancedGroup = AdvancedGroup(
        "2", studentListA, studentListB, studentListC, studentListD)

    PrintLog.info("All students")
    print(f"{advancedGroup.allStudents}")

    PrintLog.info("Set Perfect List")
    advancedGroup.setPerfectLists()

    for course, studentList in advancedGroup.studentLists.items():
        PrintLog.info(f"Lista - {course}")
        print(studentList.df)
