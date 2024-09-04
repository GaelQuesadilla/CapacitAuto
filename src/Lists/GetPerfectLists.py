from src.FileManager.AskFile import askPath
from src.Config import Config
import pandas as pd
import pprint
from .StudentList import StudentList
import pprint
from .Student import Student, getEmptyStudent


def getPerfectList(allLists: list, Semestre: str):

    emptyStudent = getEmptyStudent(Semestre)

    pprint.pp(emptyStudent)
    headersDf: pd.DataFrame = pd.DataFrame.from_dict(emptyStudent.to_dict())

    print(headersDf)


if __name__ == "__main__":
    # Lista4A = StudentList(
    #     askPath("Consiguiendo listas del 4A", suffix=".xlsx"))
    # Lista4B = StudentList(
    #     askPath("Consiguiendo listas del 4B", suffix=".xlsx"))
    # Lista4C = StudentList(
    #     askPath("Consiguiendo listas del 4C", suffix=".xlsx"))
    # Lista4D = StudentList(
    #     askPath("Consiguiendo listas del 4D", suffix=".xlsx"))
    Lista4A = "C:\\Users\\gaelg\\main\\Projects\\capacitAuto\\data\\lists\\TEST\\'Lista Alumnos 4-A.xlsx'"
    Lista4B = "C:\\Users\\gaelg\\main\\Projects\\capacitAuto\\data\\lists\\TEST\\'Lista Alumnos 4-B.xlsx'"
    Lista4C = "C:\\Users\\gaelg\\main\\Projects\\capacitAuto\\data\\lists\\TEST\\'Lista Alumnos 4-C.xlsx'"
    Lista4D = "C:\\Users\\gaelg\\main\\Projects\\capacitAuto\\data\\lists\\TEST\\'Lista Alumnos 4-D.xlsx'"

    ans = getPerfectList([Lista4A, Lista4B, Lista4C, Lista4D], "4")
    for df in ans:
        print(df.df)
