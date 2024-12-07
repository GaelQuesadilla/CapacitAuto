from src.Model.models.Group import Group
from src.Model.models.Student import Student
from src.Model.models.StudentList import StudentList
from typing import List, Dict, Any
import pandas as pd
from src.Config import Config
from src.Log import setup_logger

maxStudents: int = Config.read("School", "max_students_in_group")
optionPrefix: str = Config.read("General", "choice_name")
relevantGradesPrefix: str = Config.read("General", "relevant_grades_name")

logging = setup_logger()


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
            logging.warning(
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
            currentList.sort(
                ascending=False, by=[
                    "Promedio", relevantGradesPrefix.format(course)]
            )

    def iterate(self):
        changedLists = 0
        for course in self.courses:
            self.sortByGrades()
            currentList = self._studentLists.get(course)
            currentList.df.reset_index(drop=True, inplace=True)
            shape = currentList.df.shape

            for i in range(45, shape[0], 1):
                curp: str = currentList.df.loc[i]["CURP"]
                student: Student = currentList.getStudent(curp)

                currentChoice = student.getChoiceIndex(course)
                nextChoice = student.getChoiceName(currentChoice+1)

                nextList = self._studentLists.get(nextChoice)
                currentList.moveStudent(student=student, toList=nextList)


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

    logging.info("All students")
    print(f"{advancedGroup.allStudents}")

    logging.info("Set Perfect List")
    advancedGroup.setPerfectLists()

    logging.info("Set Perfect List")

    for course, studentList in advancedGroup.studentLists.items():
        logging.info(f"Lista - {course}")
        print(studentList.df)
