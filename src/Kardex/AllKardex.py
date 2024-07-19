from src.FileManager.AskFile import askPath
from .ReadKardex import ReadKardex
from alive_progress import alive_bar
from colorama import Fore, init
from .errors import InvalidCurp
import json
from src.Config import Config
import os
from src.FileManager.SafeFileName import safeFileName
from src.Log import Log


init(autoreset=True)

encoding = Config.read("General", "encoding")


def saveAllKardex():
    """Read CURPs from a file, get the kardex information and save the results as a json file."""
    curpsDir = askPath("Consiguiendo CURPs", suffix=".txt")
    curps = open(curpsDir, "rt").readlines()
    allKardex = []
    curpReport = []

    with alive_bar(len(curps)) as bar:
        for index, curp in enumerate(curps):
            curp = curp.replace("\n", "")
            current = ReadKardex(curp)
            try:
                info = current.getInfo()
                Log.log(
                    f"{curp}{Fore.RESET}: {info.get('Name')}, {info.get('Semester')}, {
                        info.get('Group')}, {info.get("Final_Grade")}",
                    Log.success
                )
                allKardex.append(info)
            except InvalidCurp:
                Log.log(
                    f"{curp}{Fore.RESET}: CURP NO VALIDA", Log.warning
                )
                curpReport.append(curp)

            bar()
    allKardexFileDir = os.path.join(
        Config.read("Files", "output_dir"),
        "AllKardex.json"
    )
    allKardexFileDir = safeFileName(
        "Guardando los kardex en un archivo .json...",
        allKardexFileDir
    )

    with open(allKardexFileDir, "w", encoding=encoding) as allKardexFile:
        json.dump(allKardex, allKardexFile)

    Log.log(f"Kardex guardado en {allKardexFileDir}", Log.success)

    curpReportFileDir = os.path.join(
        Config.read("Files", "reports_dir"),
        "invalidCurps.json"
    )
    curpReportFileDir = safeFileName(
        "Guardando reporte de CURPs...", curpReportFileDir
    )

    with open(curpReportFileDir, "w", encoding=encoding) as curpReportFile:
        json.dump(curpReport, curpReportFile)

    Log.log(f"Reporte de CURPs guardado en {allKardexFileDir}", Log.success)


def getAllKardex(allKardexFileDir: str = None):
    """Retrieves and returns all kardex information from 'AllKardex.json'.

    Returns
    -------
    list
        A list of dictionaries containing kardex information.
    """

    if allKardexFileDir is None:
        allKardexFileDir = askPath(
            "Cargando archivo de kardex...", Config.read("Files", "output_dir"), prefix="AllKardex", suffix=".json")
    if not allKardexFileDir is None:
        pass
    with open(allKardexFileDir, "r", encoding=encoding) as allKardexFile:
        Log.log(f"Kardex cargado desde {allKardexFileDir}", Log.success)
        return json.load(allKardexFile)


if __name__ == "__main__":
    pass
