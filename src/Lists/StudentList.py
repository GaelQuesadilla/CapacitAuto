from __future__ import annotations
from src.FileManager.AskFile import askPath
from src.Config import Config
import pandas as pd
from src.Log import Log
from src.Lists.Student import Student
from src.Lists.List import List

maxStudents = Config.read("School", "max_students_in_group")


class StudentList(List):
    def __init__(
        self,
        fileName: str,
        semester: str,
        group: str = None,
        package: str = None,
        training=None,
        maxStudents: int = maxStudents
    ):
        self._semester = semester
        self._group = group
        self._package = package
        self.training = training
        self.maxStudents = maxStudents

        voidStudent: Student = Student(Semestre=semester)
        headers = voidStudent.to_dict().keys()

        df: pd.DataFrame = pd.DataFrame(columns=headers)

        super().__init__(fileName, df)

    def moveStudent(self, CURP: str, to: StudentList):
        Log.log(Log.info, f"Moving student {CURP} from to {to}")
