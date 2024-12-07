import unittest
from src.Model.models.Student import Student
from src.Model.models.StudentList import StudentList
from src.Model.models.Group import Group
from src.test.models.utils.GenStudent import genStudent


class TestGroup(unittest.TestCase):

    def setUp(self):
        self.students_1 = [genStudent(i) for i in range(0, 10)]
        self.students_2 = [genStudent(i) for i in range(10, 20)]

        self.student_list_1 = StudentList("test_1.xlsx", "1")
        self.student_list_2 = StudentList("test_2.xlsx", "1")

        for student in self.students_1:
            self.student_list_1.addStudent(student)

        for student in self.students_2:
            self.student_list_2.addStudent(student)

        self.group = Group(
            semester="1",
            group="A",
            list1=self.student_list_1, list2=self.student_list_2
        )

    def test_group_initialization(self):
        self.assertEqual(self.group._semester, "1")
        self.assertEqual(
            self.group._studentLists["list1"], self.student_list_1)
        self.assertEqual(
            self.group._studentLists["list2"], self.student_list_2)

    def test_student_list_contents(self):
        self.assertEqual(self.group.studentLists["list1"].rows, 10)
        self.assertEqual(self.group.studentLists["list2"].rows, 10)

    def test_semester_property(self):
        self.assertEqual(self.group.semester, "1")
        self.group.semester = "2"
        self.assertEqual(self.group.semester, "2")
