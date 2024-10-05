from __future__ import annotations
from src.FileManager.AskFile import askPath
from src.Config import Config
import pandas as pd
import pprint
from src.Log import Log
from src.Lists.Student import Student


class StudentList:
    def __init__(self, fileName: str = None):
        self._fileName: str = fileName
        self._df: pd.DataFrame = pd.DataFrame()

    @property
    def fileName(self):
        return self._fileName

    @property
    def df(self):
        return self._df

    def load(self):
        self._df = pd.read_excel(self.fileName)
        print(self._df)

    def save(self):
        self._df.to_excel(self._fileName, index=False)

    def moveStudent(self, CURP: str, to: StudentList):

        Log.log(Log.info, f"Moving student {CURP} from to {to}")


if __name__ == "__main__":
    from src.FileManager.AskFile import askPath
    path: str = askPath("Getting student list for test", suffix="xlsx")

    testList: StudentList = StudentList(path)
    testList.load()
