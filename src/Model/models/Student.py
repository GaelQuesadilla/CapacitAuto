from dataclasses import dataclass, field, asdict
from src.Config import Config
from typing import Any, Dict, List
from src.Log import setup_logger


packages = Config.read("School", "packages").split(",")
trainings = Config.read("School", "trainings").split(",")

relevantGradesPrefix = Config.read("General", "relevant_grades_name")
choicesPrefix = Config.read("General", "choice_name")

logging = setup_logger()


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
    extra_fields: dict
        Extra fields
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
            logging.warning(
                f"Student {self.name} do not have attribute {name}",
                show=False
            )

        return None

    def set(self, name: str, value: Any):
        extraKeys = self.extra_fields.keys()
        primary_attrs = [
            "CURP", "Semestre", "Grupo", "Turno", "Nombre", "Promedio"
        ]

        if name in extraKeys:
            self.extra_fields[name] = value
        elif not name in extraKeys and name in primary_attrs:
            setattr(self, name, value)
        else:
            logging.warning(
                f"No es posible agregar nuevos atributos desde "
                f"set a {self.Nombre} {self.Semestre} {self.Grupo}. "
                f"Rechazando {name} = {value}",
            )

    def setExtras(self, **kwargs):
        for key, value in kwargs.items():
            self.extra_fields[key] = value

    def to_dict(self) -> Dict[str, Any]:
        default_dict: dict = asdict(self)
        default_dict = default_dict | default_dict["extra_fields"]
        default_dict.pop("extra_fields")

        return default_dict

    def getChoices(self) -> List[str]:
        courses: List[str] = []
        if self.Semestre in ["1", "2"]:
            courses = packages
        elif self.Semestre in ["3", "4"]:
            courses = trainings
        else:
            return None

        choices: Dict[str: int] = [
            {
                course: self.extra_fields.get(choicesPrefix.format(course))
            }
            for course in courses
        ]

        return choices

    def getChoiceName(self, choice: int) -> str:
        courses: List[str] = []
        if self.Semestre in ["1", "2"]:
            courses = packages
        elif self.Semestre in ["3", "4"]:
            courses = trainings
        else:
            return None

        if choice > 4:
            choice = 4

        for course in courses:
            if self.getChoiceIndex(course) == choice:
                return course

    def getChoiceIndex(self, choice: str) -> int:
        return self.extra_fields.get(choicesPrefix.format(choice))


if __name__ == "__main__":
    import pprint
    test = Student(Semestre="2")
    pprint.pp(test.to_dict())
    pprint.pp(asdict(test))
