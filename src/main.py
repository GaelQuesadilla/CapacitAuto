from src.Kardex.AllKardex import saveAllKardex
from src.Kardex.AllSubjects import AllSubjects
from src.Kardex.CalcRelevantGrades import calcRelevantGrades
from src.Lists.StudentsLists import createStudentsList
from src.Log import Log

if __name__ == "__main__":
    Log.log("Start", Log.info)

    allKardexFileDir = saveAllKardex()
    subjects = AllSubjects(allKardexFileDir)
    subjects.saveToExcel()
    calcRelevantGrades(allKardexFileDir)
    createStudentsList(allKardexFileDir)

    Log.log("End", Log.info)
