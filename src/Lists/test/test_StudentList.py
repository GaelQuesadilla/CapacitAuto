import unittest
import pandas as pd
from src.Lists.StudentList import StudentList
from src.Lists.Student import Student
from unittest.mock import patch
from src.Config import Config
import random

maxStudents = Config.read("School", "max_students_in_group")


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


class TestStudentList(unittest.TestCase):

    @patch("src.Lists.Student.Student.to_dict")
    def test_initialization(self, mock_to_dict):
        mock_to_dict.return_value = {
            "CURP": None,
            "Semestre": None,
            "Grupo": None,
            "Turno": None,
            "Nombre": None,
            "Promedio": None,
        }

        student_list = StudentList(
            "test.xlsx", "1", "A", "package", "training")

        mock_to_dict.assert_called_once()

        expected_columns = mock_to_dict.return_value.keys()
        self.assertListEqual(
            list(expected_columns),
            student_list.df.columns.tolist()
        )

        self.assertEqual(student_list._semester, "1")
        self.assertEqual(student_list._group, "A")
        self.assertEqual(student_list._package, "package")
        self.assertEqual(student_list.training, "training")
        self.assertEqual(student_list.maxStudents, maxStudents)

    def test_StudentMove(self):
        students: list = [genStudent(index) for index in range(0, 10)]

        studentList1 = StudentList("test1.xlsx", "1")
        studentList2 = StudentList("test2.xlsx", "1")

        for student in students:
            studentList1.addStudent(student)

        studentToMove: Student = students[0]

        studentList1.moveStudent(studentToMove, studentList2)

        self.assertEqual(studentList1.getStudent(studentToMove.CURP), None)

        self.assertEqual(studentList2.getStudent(
            studentToMove.CURP), studentToMove)

        # Check if the student has ben deleted from the original list
        self.assertEqual(studentList1.rows, len(students) - 1)
        # Check if the student has ben added
        self.assertEqual(studentList2.rows, 1)

    def test_StudentDelete(self):
        students: list = [genStudent(index) for index in range(0, 10)]

        studentList1 = StudentList("test1.xlsx", "1")

        for student in students:
            studentList1.addStudent(student)

        studentToDelete: Student = students[0]
        studentList1.deleteStudent(studentToDelete)

        self.assertEqual(studentList1.rows, len(students)-1)
