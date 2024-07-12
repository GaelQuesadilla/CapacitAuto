from bs4 import BeautifulSoup
from .GetStudentKardex import GetStudentKardex
from .errors import InvalidCurp
from src.config import Config
from src.Tools.GetIndexes import getIndexes
from datetime import datetime
from src.Tools.SliceList import sliceList
import math


class ReadKardex():
    def __init__(self, curp):
        self.curp = curp
        self.kardex = None
        self.soup = None
        self.info = {
            "Name": None,
            "CURP": None,
            "Semester": None,
            "Group": None,
            "Shift": None,
            "Grades": {},
            "Final_Grade": None,
        }

        self.kardex = GetStudentKardex(curp)

    def cleanSoup(self):
        cleanSoup = []
        for line in self.soup.get_text().splitlines():
            cleanLine = line

            cleanLine = cleanLine.replace("\xa0", " ")
            cleanLine = cleanLine.replace("\u200e", " ")
            cleanLine = cleanLine.replace(" ", " ")

            for _ in range(10):
                newCleanLine = cleanLine.replace("  ", " ")
                if cleanLine == newCleanLine:
                    break
                cleanLine = newCleanLine

            if cleanLine == "":
                continue
            if cleanLine == " ":
                continue

            cleanSoup.append(cleanLine)
        self.soup = cleanSoup

    def readKardex(self):
        self.soup = BeautifulSoup(self.kardex.content, "html.parser")
        self.cleanSoup()

        if len(self.soup) == 2:
            raise InvalidCurp(
                f"The Kardex application has not been able to find the curp:'{self.curp}'")

        return self.soup

    def getStudentInfo(self):

        nameIndex = self.soup.index("ALUMNO : ") + 1
        self.info["Name"] = self.soup[nameIndex]

        self.info["CURP"] = self.curp

        semesterIndex = self.soup.index("SEMESTRE : ") + 1
        self.info["Semester"] = self.soup[semesterIndex]

        groupIndex = self.soup.index("GRUPO : ") + 1
        self.info["Group"] = self.soup[groupIndex]

        self.info["Shift"] = Config.read("School", "School_shift")

        return self.info

    def getStudentGrades(self):

        firstIndex = getIndexes(self.soup, "FECHA ")[-1]+1
        last_index = getIndexes(self.soup, "Observaciones : ")[0]
        soupGrades = self.soup[firstIndex:last_index]

        currentYear = datetime.now().year

        gradesKeys = [
            f"{year}{suffix}"
            for year in range(
                currentYear-6, currentYear+1)
            for suffix in ["A", "B"]
        ]  # 2021A, 2021B, 2022A, 2022B, 2023A ...

        soupGrades = sliceList(soupGrades, *gradesKeys)

        gradesSum = 0
        gradesCount = 0
        for subject in soupGrades:
            semester = subject[1]

            if subject[3][-1] == " ":
                # In case that the subject name is divided
                subject[3] += subject[4][:-1]
                subject.remove(subject[4])

            subjectName = subject[3]

            # Select data
            AllGrades = subject[4:]

            # Get extraordinary grades
            extraordinaryGrades = []
            lastExtraordinaryIndex = None
            for index, el in enumerate(AllGrades):
                if el.find("/") > -1:
                    extraordinaryGrades.append(float(AllGrades[index-1]))
                    lastExtraordinaryIndex = index

            normalGradesSoup = AllGrades
            if not lastExtraordinaryIndex is None:
                normalGradesSoup = AllGrades[lastExtraordinaryIndex:]

            normalGrades = []
            for grade in normalGradesSoup:
                if grade.find(".") > -1 or grade == "10":
                    normalGrades.append(float(grade))

            if len(normalGrades) == 4:
                FinalGrade = normalGrades[3]
            if len(normalGrades) < 4:
                FinalGrade = sum(normalGrades)/len(normalGrades)

            grades = {
                "1": None,
                "2": None,
                "3": None,
                "Extra": None,
                "Final": None,
            }

            for index, el in enumerate(normalGrades):
                if index == 3:
                    break
                grades[str(index+1)] = el

            grades["Final"] = FinalGrade

            if len(extraordinaryGrades) > 0:
                grades["Extra"] = extraordinaryGrades[-1]
                FinalGrade = extraordinaryGrades[-1]

            if self.info.get("Grades").get(semester) is None:
                self.info["Grades"][semester] = {}

            self.info["Grades"][semester][subjectName] = grades

            gradesSum += FinalGrade
            gradesCount += 1

        self.info["Final_Grade"] = math.ceil(gradesSum*10/gradesCount)/10
        return soupGrades


if __name__ == "__main__":
    pass
