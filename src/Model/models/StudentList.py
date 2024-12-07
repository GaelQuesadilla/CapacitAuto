from __future__ import annotations
from src.Config import Config
import pandas as pd
from src.Log import setup_logger
from src.Model.models.Student import Student
from src.Model.models.DataList import DataList
from src.Model.exceptions.list_errors import TryingToDeleteAnInexistentStudent

maxStudents = Config.read("School", "max_students_in_group")

logging = setup_logger()


class StudentList(DataList):
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

    def getStudent(self, CURP: str):
        student = Student(Semestre=self._semester)

        studentData = self.df[self.df["CURP"] == CURP]

        if studentData.shape[0] == 0:
            logging.warning(
                f"La búsqueda de la CURP {CURP} en la lista {
                    self.fileName} no consigue ningún elemento"
            )
            return None

        if studentData.shape[0] > 1:
            logging.warning(
                f"La búsqueda de la CURP {CURP} en la lista {
                    self.fileName} consigue elementos duplicados"
            )

        studentDataDict: dict = studentData.iloc[0].to_dict()
        for key, value in studentDataDict.items():
            student.set(key, value)

        return student

    def addStudent(self, student: Student):
        if not student.Semestre == self._semester:
            logging.warning(
                f"El estudiante con CURP {student.CURP} tiene grado '{
                    student.Semestre}' y será agregado a la lista con grado '{self._semester}'."
            )
        self.df.loc[len(self.df)] = student.to_dict()

    def deleteStudent(self, student: Student = None):
        studentToDelete = self.getStudent(student.CURP)

        if studentToDelete == None:
            raise TryingToDeleteAnInexistentStudent

        self._df = self.df[self.df["CURP"] != student.CURP]

    def moveStudent(self, student: Student, toList: StudentList):

        toList.addStudent(student)
        self.deleteStudent(student)
        logging.info(
            f"Moving student {
                student.CURP} from {self.fileName} to {toList.fileName}"
        )

    def updateStudent(self, student: Student):
        studentToUpdate = self.getStudent(student.CURP)

        if studentToUpdate is None:
            logging.warning(
                f"El estudiante con CURP {
                    student.CURP} no fue encontrado en la lista."
            )
            return None

        # Actualiza cada campo en el DataFrame
        for key, value in student.to_dict().items():
            self.df.loc[self.df["CURP"] == student.CURP, key] = value

        logging.info(f"Estudiante con CURP {student.CURP} actualizado.")


if __name__ == "__main__":
    import pprint
    student = Student(**{
        "CURP": "GOMG060722HBSNNLA5",
        "Semestre": "1",
        "Grupo": "B",
        "Turno": "M",
        "Nombre": "GONZALEZ MENDEZ, GAEL",
        "Promedio": 9.6,
    })

    studentList = StudentList("test1.xlsx", "1")
    print("Añadiendo estudiante")
    studentList.addStudent(student=student)
    print(studentList.df)

    print("Consiguiendo estudiante")
    pprint.pp(studentList.getStudent("GOMG060722HBSNNLA5"))

    print("Eliminando estudiante")
    studentList.deleteStudent(student)

    print(studentList.df)
