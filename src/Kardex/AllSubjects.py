from .AllKardex import getAllKardex
from alive_progress import alive_bar
import pprint
import pandas as pd
import os
from src.Config import Config
from colorama import Fore, init
import numpy

init(autoreset=True)


class AllSubjects():
    def __init__(self):
        self._allSubjects = {
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
        }
        self.allSubjectsFileDir = os.path.join(
            Config.read("Files", "output_dir"),
            "AllSubjects.xlsx"
        )

        for package in Config.read("School", "packages").split(","):
            prefix = Config.read("General", "relevant_subjects_name")
            self._allSubjects[prefix.format(package)] = []

        for package in Config.read("School", "trainings").split(","):
            prefix = Config.read("General", "relevant_subjects_name")
            self._allSubjects[prefix.format(package)] = []

    def getAll(self):
        allStudents = getAllKardex()

        with alive_bar(len(allStudents)) as bar:
            for student in allStudents:
                for semester in student.get("Grades").keys():
                    subjects = student.get("Grades").get(semester).keys()
                    set1 = set(subjects)
                    set2 = set(self._allSubjects[semester])
                    self._allSubjects[semester] = list(set1.union(set2))
                bar()

        return self._allSubjects

    def saveToExcel(self):

        df = pd.DataFrame(
            dict([(k, pd.Series(v)) for k, v in self.getAll().items()])
        )

        df.to_excel(self.allSubjectsFileDir, index=False)
        print(
            f"{Fore.GREEN}[✓] All Subjects saved in: {self.allSubjectsFileDir}"
        )

        return None

    def getAllFromExcel(self):

        df = pd.read_excel(self.allSubjectsFileDir)

        print(
            f"{Fore.GREEN}[✓] All Subjects recovered from: {
                self.allSubjectsFileDir}"
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
