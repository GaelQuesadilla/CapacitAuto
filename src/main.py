from src.Kardex.AllKardex import saveAllKardex
from src.Kardex.AllSubjects import AllSubjects
from src.Kardex.CalcRelevantGrades import calcRelevantGrades
from src.Lists.StudentsLists import createStudentsList
from src.Logging.Log import Log

if __name__ == "__main__":
    Log.log("Start", Log.info)

    saveAllKardex()
    subjects = AllSubjects()
    subjects.saveToExcel()
    calcRelevantGrades()
    createStudentsList()

    Log.log("End", Log.info)
