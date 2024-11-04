import pandas as pd


class DataList:
    def __init__(self, fileName: str, df: pd.DataFrame = None):
        self._fileName: str = fileName
        self._df: pd.DataFrame = df

    @property
    def fileName(self):
        return self._fileName

    @fileName.setter
    def fileName(self, fileName: str):
        if not fileName.endswith(".xlsx"):
            fileName += ".xlsx"
        self._fileName = fileName

    @property
    def rows(self):
        return self.df.shape[0]

    @property
    def columns(self):
        return self.df.shape[1]

    @property
    def df(self):
        return self._df

    def load(self):
        self._df = pd.read_excel(self.fileName)

    def save(self):
        self._df.to_excel(self._fileName, index=False)

    def sort(self, by: list, ascending: bool = False):
        self._df = self.df.sort_values(ascending=ascending, by=by)
