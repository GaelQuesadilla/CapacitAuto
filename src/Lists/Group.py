from src.Lists.StudentList import StudentList
from typing import Dict


class Group:
    def __init__(self, semester: str, group: str = None, ** kwargs: StudentList):
        self._semester: str = semester
        self._group: str = group
        self._studentLists: Dict[str, StudentList] = kwargs

    @property
    def semester(self):
        return self._semester

    @semester.setter
    def semester(self, value):
        self._semester = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def studentLists(self):
        return self._studentLists
