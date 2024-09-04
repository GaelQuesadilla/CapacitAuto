from __future__ import annotations
from src.FileManager.AskFile import askPath
from src.Config import Config
import pandas as pd
from src.Log import Log


class StudentList:
    def __init__(self, fileName: str = None):
        self._fileName: str = fileName
        self._df: pd.DataFrame = None
        self._getList()

    @property
    def fileName(self):
        return self._fileName

    @property
    def df(self):
        return self._df

    def _getList(self):
        self._df = pd.read_excel(self.fileName)

    def moveStudent(self, CURP: str, to: StudentList):

        Log.log(Log.info, f"Moving student {CURP} from to {to}")


if __name__ == "__main__":
    pass
