from .AllKardex import getAllKardex
from alive_progress import alive_bar
import pandas as pd
import os
from src.Config import Config
from colorama import Fore, init
import numpy
from src.FileManager.SafeFileName import safeFileName
from src.FileManager.AskFile import askPath
from src.Log import PrintLog, log_function

init(autoreset=True)


class AllSubjects():
    """A class to manage and save all subjects from students kardex data

    This class provides methods to collect, process, and save information about all subjects 
    taken by students across various semesters. The subjects data can be saved to or loaded from 
    an Excel file.

    Attributes
    ----------
    _allSubjects : dict
        A dictionary to store subjects for each semester.
    allSubjectsFileDir : str
        The file path for saving and loading the subjects data in Excel format.
    _allKardexFileDir : str
        The file path for load the kardex data.

    Methods
    -------
    getAll():
        Collects all subjects from student kardex data.
    saveToExcel():
        Saves the collected subjects data to an Excel file.
    getAllFromExcel():
        Loads the subjects data from an Excel file.
    """

    def __init__(self, allKardexFileDir: str = None):
        """Initializes AllSubjects class with default values and file_paths.

        Parameters
        ----------
        allKardexFileDir : str, optional
            The path of the Kardex file to get, by default None
        """
        # TODO Añadir un directorio estático en AllSubject para evitar prompts repetidos
        self._allSubjects = {
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
        }
        self.allSubjectsFileDir = None
        self._allKardexFileDir = allKardexFileDir

        for package in Config.read("School", "packages").split(","):
            prefix = Config.read("General", "relevant_subjects_name")
            self._allSubjects[prefix.format(package)] = []

        for package in Config.read("School", "trainings").split(","):
            prefix = Config.read("General", "relevant_subjects_name")
            self._allSubjects[prefix.format(package)] = []

    @log_function
    def getAll(self):
        """Collects all subjects from students kardex data. 

        Returns
        -------
        dict
            A dict containing all subjects for each semester
        """
        allStudents = getAllKardex(self._allKardexFileDir)

        with alive_bar(len(allStudents)) as bar:
            for student in allStudents:
                for semester in student.get("Grades").keys():
                    subjects = student.get("Grades").get(semester).keys()
                    set1 = set(subjects)
                    set2 = set(self._allSubjects[semester])
                    self._allSubjects[semester] = list(set1.union(set2))
                bar()

        return self._allSubjects

    @log_function
    def saveToExcel(self):
        """Collect and save all subjects data into an Excel file.

        This method get all subjects and converts _allSubjects dictionary to a pandas DataFrame and saves it to an Excel file 
        """
        self.allSubjectsFileDir = safeFileName(
            "Guardando Excel con todas las materias...",
            os.path.join(
                Config.read("Files", "data_dir"),
                "AllSubjects.xlsx")
        )

        df = pd.DataFrame(
            dict([(k, pd.Series(v)) for k, v in self.getAll().items()])
        )

        df.to_excel(self.allSubjectsFileDir, index=False)
        PrintLog.success(
            f"Todas las materias han sido guardadas en: {
                self.allSubjectsFileDir}"
        )

    @log_function
    def getAllFromExcel(self):
        """Loads the subjects data from an Excel file.

        Returns
        -------
        dict
            A dictionary that contains all subjects for each semester.
        """

        self.allSubjectsFileDir = askPath(
            "Consiguiendo tabla de excel con todas las materias ", Config.read("Files", "data_dir"), prefix="AllSubjects", suffix="xlsx")

        df = pd.read_excel(self.allSubjectsFileDir)

        PrintLog.success(
            f"Materias recuperadas desde: {
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
