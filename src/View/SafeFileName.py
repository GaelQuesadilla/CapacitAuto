import datetime
import os

from src.utils.Normalize import normalizeText
from .AskFile import askPath
from src.Log import setup_logger, trackFunction

logging = setup_logger()


@trackFunction
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

    logging.info(info)
    path = os.path.join(path)

    if not os.path.exists(path):
        return path

    if os.path.exists(path):
        logging.warning(
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

    logging.info(f"Ruta seleccionada: {newPath}")
    return newPath


if __name__ == "__main__":
    pass
