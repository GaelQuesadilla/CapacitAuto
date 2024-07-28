from src.Kardex.AllKardex import saveAllKardex
from src.Kardex.AllSubjects import AllSubjects
from src.Kardex.CalcRelevantGrades import calcRelevantGrades
from src.Lists.StudentsLists import createStudentsList
from src.Tools.GetIndexes import getIndexes
from src.Tools.Normalize import normalizeText
from src.Tools.SliceList import getIndexes, sliceList
from src.Log import Log, log_function
from src.Config import Config
from src.FileManager.AskFile import askPath
from src.FileManager.GetListDirs import getListDirs
from src.FileManager.SafeFileName import safeFileName

from colorama import Fore, init
from IPython import embed


init(autoreset=True)


@log_function
def main():
    print(f"{Fore.MAGENTA}RUNNING SHELL")
    embed()


if __name__ == "__main__":
    main()
