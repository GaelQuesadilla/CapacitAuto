from src.Config import Config
from .AllKardex import getAllKardex
from alive_progress import alive_bar
from .AllSubjects import AllSubjects
import pprint
import math
import os
import json


def calcRelevantGrades():
    allKardex = getAllKardex()
    subjects = AllSubjects()
    allSubjects = subjects.getAllFromExcel()

    options = Config.read(
        "School", "packages").split(",") + Config.read(
        "School", "trainings").split(",")

    with alive_bar(len(allKardex)) as bar:
        for student in allKardex:

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

            bar()
    allKardexFileDir = os.path.join(
        Config.read("Files", "output_dir"),
        "AllKardex.json"
    )
    encoding = Config.read("General", "encoding")
    with open(allKardexFileDir, "w", encoding=encoding) as allKardexFile:
        json.dump(allKardex, allKardexFile)

    return None


if __name__ == "__main__":
    pass
