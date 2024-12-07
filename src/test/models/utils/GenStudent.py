
from src.Model.models.Student import Student
import random


def genStudent(index: int):

    student = Student(**{
        "CURP": f"id{index}-GOMG060722HBSNNLA5",
        "Semestre": "1",
        "Grupo": "B",
        "Turno": "M",
        "Nombre": f"{index}GONZALEZ MENDEZ, GAEL",
        "Promedio": random.randrange(5, 10),
    })

    return student
