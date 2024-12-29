from .AllKardex import AllKardex
import pandas as pd
import os
from src.Config import Config
from src.Log import setup_logger, trackFunction

logging = setup_logger()


class AllSubjects():

    def __init__(self, kardexFileName: str = None, allSubjectsFileName: str = None):

        self._allSubjects = {
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
        }
        self.allSubjectsFileDir = allSubjectsFileName
        self._allKardexFileName = kardexFileName
        self._allKardex = AllKardex(fileName=kardexFileName)

        for package in Config.read("School", "packages").split(","):
            prefix = Config.read("General", "relevant_subjects_name")
            self._allSubjects[prefix.format(package)] = []

        for package in Config.read("School", "trainings").split(","):
            prefix = Config.read("General", "relevant_subjects_name")
            self._allSubjects[prefix.format(package)] = []

    @trackFunction
    def getAll(self):
        self._allKardex.loadAllKardex()
        allStudents = self._allKardex.allKardex

        for student in allStudents:
            for semester in student.get("Grades").keys():
                subjects = student.get("Grades").get(semester).keys()
                set1 = set(subjects)
                set2 = set(self._allSubjects[semester])
                self._allSubjects[semester] = list(set1.union(set2))

        return self._allSubjects

    @trackFunction
    def saveToExcel(self):

        df = pd.DataFrame(
            dict([(k, pd.Series(v)) for k, v in self.getAll().items()])
        )

        df.to_excel(self.allSubjectsFileDir, index=False)
        logging.info(
            f"Todas las materias han sido guardadas en: "
            f"{self.allSubjectsFileDir}"
        )

    @trackFunction
    def getAllFromExcel(self):
        """Loads the subjects data from an Excel file.

        Returns
        -------
        dict
            A dictionary that contains all subjects for each semester.
        """

        df = pd.read_excel(self.allSubjectsFileDir)

        logging.info(
            f"Materias recuperadas desde: "
            f"{self.allSubjectsFileDir}"
        )

        allSubjectsFromExcel = df.to_dict()

        for semester in allSubjectsFromExcel.keys():
            subjects = list(allSubjectsFromExcel.get(semester).values())
            for subject in subjects:
                if pd.isna(subject):
                    continue
                self._allSubjects[semester].append(subject)

        return self._allSubjects


if __name__ == "__main__":
    pass
