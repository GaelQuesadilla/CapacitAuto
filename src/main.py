from src.Kardex.AllKardex import saveAllKardex
from src.Kardex.AllSubjects import AllSubjects
from src.Kardex.CalcRelevantGrades import calcRelevantGrades
from src.Lists.StudentsLists import createStudentsList
from src.Log import PrintLog

if __name__ == "__main__":
    PrintLog.info("Start")
    allKardexFileDir = saveAllKardex()
    subjects = AllSubjects(allKardexFileDir)
    subjects.saveToExcel()
    calcRelevantGrades(allKardexFileDir)
    createStudentsList(allKardexFileDir)

    PrintLog.info("End")
