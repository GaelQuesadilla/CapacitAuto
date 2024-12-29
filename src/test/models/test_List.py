from unittest import TestCase
from src.Model.models.DataList import DataList
import pathlib


class test_List(TestCase):
    # List.xlsx
    # +---------+---------+---------+
    # | HEADER 1| HEADER 2| HEADER 3|
    # +---------+---------+---------+
    # |    1    |    6    |   11    |
    # |    2    |    7    |   12    |
    # |    3    |    8    |   13    |
    # |    4    |    9    |   14    |
    # |    5    |   10    |   15    |
    # +---------+---------+---------+
    def test_open(self):

        listPath = pathlib.Path("src") / "test" / \
            "models" / "utils" / "List.xlsx"
        list.load()

        self.assertEqual(list.df.shape, (5, 3))

        expected_first_row = [1, 6, 11]
        self.assertListEqual(list.df.loc[0].tolist(), expected_first_row)

        expected_last_row = [5, 10, 15]
        self.assertListEqual(list.df.loc[4].tolist(), expected_last_row)
