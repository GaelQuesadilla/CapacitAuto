import unittest
import pandas as pd
from src.Lists.StudentList import StudentList
from src.Lists.Student import Student
from unittest.mock import patch
from src.Config import Config

maxStudents = Config.read("School", "max_students_in_group")


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
