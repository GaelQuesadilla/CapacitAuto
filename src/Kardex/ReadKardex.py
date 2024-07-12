from bs4 import BeautifulSoup
from .GetStudentKardex import GetStudentKardex
from .errors import InvalidCurp
from src.config import Config


class ReadKardex():
    def __init__(self, curp):
        self.curp = curp
        self.kardex = None
        self.soup = None
        self.info = None

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
        self.info = {
            "Name": None,
            "CURP": None,
            "Semester": None,
            "Group": None,
            "Shift": None,
            "Grades": [],
            "Final_Grades": None,
        }

        nameIndex = self.soup.index("ALUMNO : ") + 1
        self.info["Name"] = self.soup[nameIndex]

        self.info["CURP"] = self.curp

        semesterIndex = self.soup.index("SEMESTRE : ") + 1
        self.info["Semester"] = self.soup[semesterIndex]

        groupIndex = self.soup.index("GRUPO : ") + 1
        self.info["Group"] = self.soup[groupIndex]

        self.info["Shift"] = Config.read("School", "School_shift")

        return self.info


if __name__ == "__main__":
    pass
