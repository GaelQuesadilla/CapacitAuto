import datetime
import os
from colorama import Fore, init
from src.Tools.Normalize import normalizeText
from .AskFile import askPath
init(autoreset=True)


def safeFileName(path: str):
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
    path = os.path.join(path)

    if not os.path.exists(path):
        return path

    if os.path.exists(path):
        print(
            f"{Fore.YELLOW}[⚠] The file '{
                path}' already exists, do you want to overwrite it?"
        )
        option = input(f"[Y/N]\n")
        option = option.lower()
        option = normalizeText(option)

        if option in ["y", "yes", "si", "s"]:
            return path
        if option in ["n", "no"]:
            baseDir = os.path.dirname(path)
            fileName = os.path.basename(path)
            name, extension = os.path.splitext(fileName)

            now = datetime.datetime.now()

            newFileName = f"{name}_{now.strftime(
                '%y-%m-%d_%H-%M-%S')}{extension}"

            newPath = os.path.join(baseDir, newFileName)

            print(f"{Fore.BLUE}File name: {newPath}")
            return newPath


if __name__ == "__main__":
    for _ in range(0, 10):
        path = askPath()
        print(safeFileName(path))
