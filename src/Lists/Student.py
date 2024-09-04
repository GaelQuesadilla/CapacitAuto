from dataclasses import dataclass
from src.Config import Config
from src.Tools.Normalize import normalizeText
import pprint
from typing import Any
from src.Log import Log
import pprint


packages = Config.read("School", "packages").split(",")
trainings = Config.read("School", "trainings").split(",")

relevantGradesPrefix = Config.read("General", "relevant_grades_name")
choicesPrefix = Config.read("General", "choice_name")


@dataclass
class Student:
    """Dataclass for student info

    Parameters
    ----------
    Curp: str
        The student's CURP
    Nombre: str 
        The student's Name
    Promedio: float
        The student's average
    Semester: int
        The student's semester
    Grupo: str
        The student's group
    Turno: str
        The student's shift
    """

    CURP: str = None
    Semestre: str = None
    Grupo: str = None
    Turno: str = None
    Nombre: str = None
    Promedio: float = None

    def __post_init__(self):
        if self.Semestre in ["1", "2"]:
            self._set_attributes(packages, choicesPrefix)
            self._set_attributes(packages, relevantGradesPrefix)

        if self.Semestre in ["3", "4"]:
            self._set_attributes(trainings, choicesPrefix)
            self._set_attributes(trainings, relevantGradesPrefix)

    def _set_attributes(self, items: list, prefix: str):
        for item in items:
            setattr(self, prefix.format(item), None)

    def get(self, name: str) -> Any:
        if hasattr(self, name):
            return getattr(self, name)
        else:
            Log.log(
                f"Student {self.name} do not have attribute {name}",
                Log.warning,
                show=False
            )

        return None

    def set(self, name: str, value: Any):
        setattr(self, name, value)

    def to_dict(self):
        return self.__dict__


def getEmptyStudent(Semestre: int):

    emptyStudent: Student = Student(
        CURP=None,
        Semestre=Semestre,
        Grupo=None,
        Turno=None,
        Nombre=None,
        Promedio=None
    )

    return emptyStudent


if __name__ == "__main__":
    pass
