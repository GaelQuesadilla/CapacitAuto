from src.Model.models.Student import Student
from src.Config import Config
from unittest import TestCase


class test_Student(TestCase):

    relevantGradesPrefix: str = Config.read("General", "relevant_grades_name")
    choicePrefix: str = Config.read("General", "choice_name")
    packages: list = Config.read("School", "packages").split(",")
    trainings: list = Config.read("School", "trainings").split(",")

    def test_Student_5(self):
        mock = {
            "CURP": "GOMG060722HBSNNLA5",
            "Semestre": "5",
            "Grupo":	"D",
            "Turno": "M",
            "Nombre": "González Méndez, Gael",
            "Promedio":	9.60
        }

        ans = Student(**mock).to_dict()

        self.assertTrue(ans.get("CURP") == "GOMG060722HBSNNLA5")
        self.assertTrue(ans.get("Semestre") == "5")
        self.assertTrue(ans.get("Grupo") == "D")
        self.assertTrue(ans.get("Turno") == "M")
        self.assertTrue(ans.get("Nombre") == "González Méndez, Gael")
        self.assertTrue(ans.get("Promedio") == 9.60)

        # ?  Students in the fifth semester already have a package, so they do not participate in the selection process.
        for package in self.packages:
            self.assertFalse(self.relevantGradesPrefix.format(
                package) in ans.keys())

            self.assertFalse(self.choicePrefix.format(
                package) in ans.keys())

        # ?  Students in the fifth semester already have a training, so they do not participate in the selection process.
        for training in self.trainings:
            self.assertFalse(self.relevantGradesPrefix.format(
                training) in ans.keys())

            self.assertFalse(self.choicePrefix.format(
                training) in ans.keys())

    def test_Student_3(self):
        mock = {
            "CURP": "GOMG060722HBSNNLA5",
            "Semestre": "3",
            "Grupo":	"D",
            "Turno": "M",
            "Nombre": "González Méndez, Gael",
            "Promedio":	9.60
        }

        ans = Student(**mock).to_dict()

        self.assertTrue(ans.get("CURP") == "GOMG060722HBSNNLA5")
        self.assertTrue(ans.get("Semestre") == "3")
        self.assertTrue(ans.get("Grupo") == "D")
        self.assertTrue(ans.get("Turno") == "M")
        self.assertTrue(ans.get("Nombre") == "González Méndez, Gael")
        self.assertTrue(ans.get("Promedio") == 9.60)

        # ? Check if packages included in the dictionary
        for training in self.trainings:
            self.assertTrue(self.relevantGradesPrefix.format(
                training) in ans.keys())

            self.assertTrue(self.choicePrefix.format(
                training) in ans.keys())

        # ? Check if trainings are not included in the dictionary
        # ? Students apply for training in the second semester, but not for the training program.
        for package in self.packages:
            self.assertFalse(self.relevantGradesPrefix.format(
                package) in ans.keys())

            self.assertFalse(self.choicePrefix.format(
                package) in ans.keys())

    def test_Student_1(self):
        mock = {
            "CURP": "GOMG060722HBSNNLA5",
            "Semestre": "1",
            "Grupo":	"D",
            "Turno": "M",
            "Nombre": "González Méndez, Gael",
            "Promedio":	9.60
        }

        ans = Student(**mock).to_dict()

        self.assertTrue(ans.get("CURP") == "GOMG060722HBSNNLA5")
        self.assertTrue(ans.get("Semestre") == "1")
        self.assertTrue(ans.get("Grupo") == "D")
        self.assertTrue(ans.get("Turno") == "M")
        self.assertTrue(ans.get("Nombre") == "González Méndez, Gael")
        self.assertTrue(ans.get("Promedio") == 9.60)

        # ? Check if packages included in the dictionary
        for package in self.packages:
            self.assertTrue(self.relevantGradesPrefix.format(
                package) in ans.keys())

            self.assertTrue(self.choicePrefix.format(
                package) in ans.keys())

        # ? Check if trainings are not included in the dictionary
        # ? Students apply for training in the second semester, but not for the training program.

        for training in self.trainings:
            self.assertFalse(self.relevantGradesPrefix.format(
                training) in ans.keys())

            self.assertFalse(self.choicePrefix.format(
                training) in ans.keys())
