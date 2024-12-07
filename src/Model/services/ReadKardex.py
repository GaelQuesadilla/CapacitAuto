from bs4 import BeautifulSoup
from .GetStudentKardex import GetStudentKardex
from src.Model.exceptions.invalid_curp_error import InvalidCurp
from src.Config import Config
from src.utils.GetIndexes import getIndexes
from datetime import datetime
from src.utils.SliceList import sliceList
import math
from src.utils.Normalize import normalizeText


class ReadKardex():
    """Class to read and process a student's kardex information

    Attributes
    ----------
    curp : str
        The CURP (Clave Única de Registro de Población) of the student.
    _kardex : requests.Response
        The HTTP response object containing the student's kardex data.
    _soup : BeautifulSoup or list
        The parsed HTML content of the kardex data.
    _info : dict
        A dictionary to store the extracted student information.

    Methods
    -------
    _cleanSoup():
        Cleans the parsed HTML content by removing unwanted characters and empty lines.
    _readKardex():
        Parses the kardex HTML content and cleans it.
    _getStudentInfo():
        Extracts and returns the student's basic information (name, CURP, semester, group, shift).
    _getStudentGrades():
        Extracts and returns the student's grades for each subject in each semester.
    getInfo():
        Fetches and processes the student's kardex data, returning the extracted information.
    """

    def __init__(self, curp: str):
        """Initializes the class with default values

        Parameters
        ----------
        curp : str
            The student's CURP
        """
        self.curp = curp
        self._kardex = None
        self._soup = None
        self._info = {
            "Name": None,
            "CURP": None,
            "Semester": None,
            "Group": None,
            "Shift": None,
            "Grades": {},
            "Final_Grade": None,
            "Relevant_Grades": {}
        }

        for package in Config.read("School", "packages").split(","):
            prefix = Config.read("General", "relevant_grades_name")
            self._info["Relevant_Grades"][prefix.format(package)] = None

        for package in Config.read("School", "trainings").split(","):
            prefix = Config.read("General", "relevant_grades_name")
            self._info["Relevant_Grades"][prefix.format(package)] = None

    def _cleanSoup(self):
        """Cleans the parsed HTML content by removing unwanted characters and empty lines."""
        cleanSoup = []
        for line in self._soup.get_text().splitlines():
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
        self._soup = cleanSoup

    def _readKardex(self):
        """Parses the kardex HTML and cleans it.

        Returns
        -------
        list
            A list of cleaned strings extracted from the kardex HTML content.

        Raises
        ------
        InvalidCurp
            If the kardex cannot be found for the given CURP
        """
        self._soup = BeautifulSoup(self._kardex.content, "html.parser")
        self._cleanSoup()

        if len(self._soup) == 2:
            raise InvalidCurp(
                f"The Kardex application has not been able to find the curp:'{self.curp}'")

        return self._soup

    def _getStudentInfo(self):

        nameIndex = self._soup.index("ALUMNO : ") + 1
        self._info["Name"] = self._soup[nameIndex]

        self._info["CURP"] = self.curp

        semesterIndex = self._soup.index("SEMESTRE : ") + 1
        self._info["Semester"] = self._soup[semesterIndex]

        groupIndex = self._soup.index("GRUPO : ") + 1
        self._info["Group"] = self._soup[groupIndex]

        self._info["Shift"] = Config.read("School", "School_shift")

        return self._info

    def _getStudentGrades(self):

        firstIndex = getIndexes(self._soup, "FECHA ")[-1]+1
        last_index = getIndexes(self._soup, "Observaciones : ")[0]
        soupGrades = self._soup[firstIndex:last_index]

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

            subjectName = normalizeText(subject[3])

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

            if self._info.get("Grades").get(semester) is None:
                self._info["Grades"][semester] = {}

            self._info["Grades"][semester][subjectName] = grades

            gradesSum += FinalGrade
            gradesCount += 1

        self._info["Final_Grade"] = math.ceil(gradesSum*10/gradesCount)/10
        return soupGrades

    def getInfo(self):
        """Fetches and process the students kardex returning the extracted information.

        Returns
        -------
        dict
            A dictionary containing all the student's information and grades.
        """
        self._kardex = GetStudentKardex(self.curp)
        self._readKardex()
        self._getStudentInfo()
        self._getStudentGrades()
        return self._info


if __name__ == "__main__":
    pass
