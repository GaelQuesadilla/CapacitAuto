from src.FileManager.AskFile import askPath
from .ReadKardex import ReadKardex
from alive_progress import alive_bar
from colorama import Fore, init
from .errors import InvalidCurp
import json
from src.Config import Config
import os
from src.FileManager.SafeFileName import safeFileName
from src.Log import PrintLog, log_function


init(autoreset=True)

encoding = Config.read("General", "encoding")


@log_function
def saveAllKardex():
    """Read CURPs from a file, get the kardex information and save the results as a json file.

    Returns
    -------
    str
        The kardex file path
    """
    # TODO añadir condicional para evitar repetir alumnos
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
                PrintLog.success(
                    f"{curp}{Fore.RESET}: {info.get('Name')}, {info.get('Semester')}, {
                        info.get('Group')}, {info.get("Final_Grade")}"
                )
                allKardex.append(info)
            except InvalidCurp:
                PrintLog.warning(
                    f"{curp}{Fore.RESET}: CURP NO VALIDA"
                )
                curpReport.append(curp)

            bar()
    allKardexFileDir = os.path.join(
        Config.read("Files", "data_dir"),
        "AllKardex.json"
    )
    allKardexFileDir = safeFileName(
        "Guardando los kardex en un archivo .json...",
        allKardexFileDir
    )

    with open(allKardexFileDir, "w", encoding=encoding) as allKardexFile:
        json.dump(allKardex, allKardexFile)

    PrintLog.success(f"Kardex guardado en {allKardexFileDir}")

    curpReportFileDir = os.path.join(
        Config.read("Files", "reports_dir"),
        "CURPS INVALIDAS.txt"
    )

    PrintLog.info("Guardando reporte de CURPS...")

    with open(curpReportFileDir, "w", encoding=encoding) as curpReportFile:
        curpReportFile.write("\n".join(curpReport))

    PrintLog.success(f"Reporte de CURPs guardado en {curpReportFileDir}")

    return allKardexFileDir


@log_function
def getAllKardex(allKardexFileDir: str = None):
    """Retrieves and returns all kardex information from 'AllKardex.json'.

    Parameters
    ----------
    allKardexFileDir : str, optional
        The path of the Kardex file to get, by default None

    Returns
    -------
    list
        A list of dictionaries containing kardex information.
    """

    if allKardexFileDir is None:
        allKardexFileDir = askKardexPath()

    if not allKardexFileDir is None:
        pass
    with open(allKardexFileDir, "r", encoding=encoding) as allKardexFile:
        PrintLog.success(f"Kardex cargado desde {allKardexFileDir}")
        return json.load(allKardexFile)


def askKardexPath():
    """Ask the path of the kardex file

    Returns
    -------
    str
        The path of the kardex file
    """
    allKardexFileDir: str = askPath(
        "Cargando archivo de kardex...", Config.read("Files", "data_dir"), prefix="AllKardex", suffix=".json")
    return allKardexFileDir


if __name__ == "__main__":
    pass
