import unittest
from src.Lists.Group import Group
from src.Lists.Student import Student
from src.Lists.StudentList import StudentList
from src.Lists.AdvancedGroup import AdvancedGroup
from src.Lists.test.GenStudent import genStudent
from typing import List
from src.Config import Config


class TestAdvancedGroup(unittest.TestCase):

    def setUp(self):
        self.students_1: List[Student] = [genStudent(i) for i in range(0, 45)]
        self.students_2: List[Student] = [genStudent(i) for i in range(45, 90)]

        # Inicializar las listas de estudiantes
        self.student_list_1 = StudentList(
            semester="1", fileName="test_1.xlsx", group="A")
        self.student_list_2 = StudentList(
            semester="1", fileName="test_2.xlsx", group="B")

        # Agregar los estudiantes a sus respectivas listas
        for student in self.students_1:
            self.student_list_1.addStudent(student)
        for student in self.students_2:
            self.student_list_2.addStudent(student)

        # Inicializar AdvancedGroup con listas de estudiantes y semestre
        self.advanced_group = AdvancedGroup("1",
                                            *[self.student_list_1, self.student_list_2, ])

    def test_initialization(self):
        self.assertEqual(
            self.advanced_group.courses,
            Config.read("School", "packages").split(",")
        )

        self.assertEqual(self.advanced_group.group, "Capacitaciones")
        self.assertEqual(self.advanced_group.semester, "1")

    def test_all_students_property(self):
        # Verifica que la propiedad allStudents devuelve los estudiantes concatenados
        # Concatenar las listas de estudiantes
        all_students_list: List[Student] = self.students_1 + self.students_2
        all_students_df: StudentList = StudentList(
            fileName=None, group=None, maxStudents=None, package=None, semester="1", training=None)

        for student in all_students_list:
            all_students_df.addStudent(student)

        self.assertEqual(
            self.advanced_group.allStudents.to_dict(),
            all_students_df.df.to_dict()
        )

    def test_groups_creation(self):
        # Verifica que las listas de estudiantes se crean correctamente para cada curso

        packages = Config.read("School", "packages").split(",")

        print(f"{packages=}")
        print(f"{self.advanced_group.courses=}")
        print(f"{self.advanced_group.studentLists=}")
        for package in packages:
            self.assertTrue(package in self.advanced_group.courses)
            self.assertTrue(package in self.advanced_group.studentLists.keys())
