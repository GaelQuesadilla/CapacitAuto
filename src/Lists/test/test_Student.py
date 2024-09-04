from src.Lists.Student import Student
import pprint
from unittest import TestCase


class test_Student(TestCase):

    def test_Student_6(self):
        mock = {
            "CURP": "GOMG060722HBSNNLA5",
            "Semestre": "6",
            "Grupo":	"D",
            "Turno": "M",
            "Nombre": "González Méndez, Gael",
            "Promedio":	9.60
        }

        ans = Student(**mock)

        self.assertTrue(ans.CURP == "GOMG060722HBSNNLA5")
        self.assertTrue(ans.Semestre == "6")
        self.assertTrue(ans.Grupo == "D")
        self.assertTrue(ans.Turno == "M")
        self.assertTrue(ans.Nombre == "González Méndez, Gael")
        self.assertTrue(ans.Promedio == 9.60)

    def test_Student_5(self):
        mock = {
            "CURP": "GOMG060722HBSNNLA5",
            "Semestre": "5",
            "Grupo":	"D",
            "Turno": "M",
            "Nombre": "González Méndez, Gael",
            "Promedio":	9.60
        }

        ans = Student(**mock)

        self.assertTrue(ans.CURP == "GOMG060722HBSNNLA5")
        self.assertTrue(ans.Semestre == "5")
        self.assertTrue(ans.Grupo == "D")
        self.assertTrue(ans.Turno == "M")
        self.assertTrue(ans.Nombre == "González Méndez, Gael")
        self.assertTrue(ans.Promedio == 9.60)
