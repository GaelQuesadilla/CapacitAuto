import datetime
import os
from colorama import Fore, init
from src.Tools.Normalize import normalizeText
from .AskFile import askPath
from src.Log import PrintLog, log_function
init(autoreset=True)


@log_function
def safeFileName(info: str, path: str):
    """Prompts the user to ask if they want to overwrite a file

    Asks the user if they want to overwrite a file, if not, returns a unique path using datetime

    Parameters
    ----------
    path : str
        The file name

    Returns
    -------
    str
        The new file name
    """

    PrintLog.info(info)
    path = os.path.join(path)

    if not os.path.exists(path):
        return path

    if os.path.exists(path):
        PrintLog.warning(
            f"El archivo '{
                path}' ya existe ¿Desea remplazarlo?"
        )
        option = input(f"[Si/No]\n")
        option = option.lower()
        option = normalizeText(option)

        if option in ["y", "yes", "si", "s"]:
            newPath = path
        if option in ["n", "no"]:
            baseDir = os.path.dirname(path)
            fileName = os.path.basename(path)
            name, extension = os.path.splitext(fileName)

            now = datetime.datetime.now()

            newFileName = f"{name}_{now.strftime(
                '%y-%m-%d_%H-%M-%S')}{extension}"

            newPath = os.path.join(baseDir, newFileName)

    PrintLog.info(f"Ruta seleccionada: {newPath}")
    return newPath


if __name__ == "__main__":
    pass
