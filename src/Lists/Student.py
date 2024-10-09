from dataclasses import dataclass, field, asdict
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
    extra_fields: dict = field(default_factory=dict, init=False)

    def __post_init__(self, **kwargs):
        if self.Semestre in ["1", "2"]:
            self._set_attributes(packages, choicesPrefix)
            self._set_attributes(packages, relevantGradesPrefix)

        if self.Semestre in ["3", "4"]:
            self._set_attributes(trainings, choicesPrefix)
            self._set_attributes(trainings, relevantGradesPrefix)

        for kwarg, value in kwargs:
            self.set(kwarg, value)

    def _set_attributes(self, items: list, prefix: str):
        for item in items:
            if not prefix.format(item) in list(self.extra_fields.keys()):
                self.extra_fields[prefix.format(item)] = None

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
        extraKeys = self.extra_fields.keys()

        if name in extraKeys:
            self.extra_fields[name] = value
        elif not name in extraKeys:
            setattr(self, name, value)

    def setExtras(self, **kwargs):
        for key, value in kwargs:
            self.default_factory[key] = value

    def to_dict(self):
        default_dict: dict = asdict(self)
        default_dict = default_dict | default_dict["extra_fields"]
        default_dict.pop("extra_fields")

        return default_dict


if __name__ == "__main__":
    test = Student(Semestre="1")
    pprint.pp(test.to_dict())
    pprint.pp(asdict(test))
