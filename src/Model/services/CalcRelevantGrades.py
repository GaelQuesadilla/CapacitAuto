from src.Config import Config
from src.Model.services.AllKardex import AllKardex
from alive_progress import alive_bar
from src.Model.services.AllSubjects import AllSubjects
import math
import os
import json
from src.Log import setup_logger, trackFunction


@trackFunction
def calcRelevantGrades(
        allKardexFileDir: str = Config.read("Files", "all_kardex_dir"),
        allSubjectsFileDir: str = Config.read("Files", "all_subjects_dir")
):
    """Calculates relevant grades for each student based on specified subjects and saves them in a json file

    Parameters
    ----------
    allKardexFileDir : str, optional
        The path of the Kardex file to get, by default None
    """
    allKardex = AllKardex(fileName=allKardexFileDir)
    allKardex.loadAllKardex()
    subjects = AllSubjects(allSubjectsFileName=allSubjectsFileDir)
    allSubjects = subjects.getAllFromExcel()

    options = Config.read(
        "School", "packages").split(",") + Config.read(
        "School", "trainings").split(",")

    for student in allKardex.allKardex:

        for option in options:
            gradesSum = 0
            gradesCount = 0
            relevantSubjectsKey = Config.read(
                "General", "relevant_subjects_name").format(option)
            relevantSubjects = allSubjects.get(relevantSubjectsKey)

            for subjectsInSemester in student.get("Grades").values():
                for subject in subjectsInSemester:
                    if subject in relevantSubjects:
                        grades = subjectsInSemester.get(subject)

                        if grades.get("Extra") is None:
                            gradesSum += grades.get("Final")
                        else:
                            gradesSum += grades.get("Extra")
                        gradesCount += 1

            relevantGradeKey = Config.read(
                "General", "relevant_grades_name").format(option)
            if gradesCount == 0:
                relevantGrade = 0
            else:
                relevantGrade = math.ceil(gradesSum*10/gradesCount)/10
            student["Relevant_Grades"][relevantGradeKey] = relevantGrade

    encoding = Config.read("General", "encoding")
    with open(allKardexFileDir, "w", encoding=encoding) as allKardexFile:
        json.dump(allKardex.allKardex, allKardexFile)


if __name__ == "__main__":
    calcRelevantGrades(
        Config.read("Files", "all_kardex_dir"),
        Config.read("Files", "all_subjects_dir")
    )
