from src.Lists.Group import Group
from src.Lists.Student import Student
from src.Lists.StudentList import StudentList
from typing import List, Dict
from dataclasses import dataclass
import pandas as pd
from src.Config import Config
from src.Log import Log

maxStudents = Config.read("School", "max_students_in_group")


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
            Log.log(
                "Advanced groups should be used only in 1,2,3,4 semesters", Log.warning)

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
