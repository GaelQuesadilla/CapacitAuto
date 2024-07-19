from src.FileManager.AskFile import askPath
from .ReadKardex import ReadKardex
import pprint
from alive_progress import alive_bar
from colorama import Fore, init
from .errors import InvalidCurp
import json
from src.Config import Config
import os
import pprint

init(autoreset=True)

encoding = Config.read("General", "encoding")


def saveAllKardex():
    """Read CURPs from a file, get the kardex information and save the results as a json file."""
    curpsDir = askPath()
    curps = open(curpsDir, "rt").readlines()
    allKardex = []
    curpReport = []

    with alive_bar(len(curps)) as bar:
        for index, curp in enumerate(curps):
            curp = curp.replace("\n", "")
            current = ReadKardex(curp)
            try:
                info = current.getInfo()
                print(
                    f"{Fore.GREEN}[✓]{curp}{Fore.RESET}: {info.get('Name')}, {info.get('Semester')}, {
                        info.get('Group')}, {info.get("Final_Grade")}"
                )
                allKardex.append(info)
            except InvalidCurp:
                print(
                    f"{Fore.RED}[✘]{curp}{Fore.RESET}: Invalid CURP"
                )
                curpReport.append(curp)

            bar()

    allKardexFileDir = os.path.join(
        Config.read("Files", "output_dir"),
        "AllKardex.json"
    )

    with open(allKardexFileDir, "w", encoding=encoding) as allKardexFile:
        json.dump(allKardex, allKardexFile)

    curpReportFileDir = os.path.join(
        Config.read("Files", "reports_dir"),
        "invalidCurps.json"
    )

    with open(curpReportFileDir, "w", encoding=encoding) as curpReportFile:
        json.dump(curpReport, curpReportFile)


def getAllKardex():
    """Retrieves and returns all kardex information from 'AllKardex.json'.

    Returns
    -------
    list
        A list of dictionaries containing kardex information.
    """
    allKardexFileDir = os.path.join(
        Config.read("Files", "output_dir"),
        "AllKardex.json"
    )
    with open(allKardexFileDir, "r", encoding=encoding) as allKardexFile:
        return json.load(allKardexFile)


if __name__ == "__main__":
    pass
