from src.Config import Config
from colorama import init, Fore, Back
import os
from .errors import InvalidInput

init(autoreset=True)


def askPath(baseDir: str = Config.read("Files", "data_dir")):
    """Prompts the user to select a file from a directory.

    Parameters
    ----------
    baseDir : str, optional
        The base directory to list files from, by default Config.read("Files", "data_dir")

    Returns
    -------
    str
        The selected file path.

    Raises
    ------
    InvalidInput
        If the selected index is out of range
    """
    baseDir = os.path.join(baseDir)
    print(f"Files in: {Fore.YELLOW}{baseDir}")
    listdir = os.listdir(baseDir)

    def centerChar(string, n=5):
        string = str(string)
        return string.center(n, " ")

    parent = os.path.dirname(baseDir)
    print(
        f"{Back.YELLOW +
            Fore.BLACK}{centerChar("-1")}{Back.RESET + Fore.RESET}: {parent}"
    )

    for index, el in enumerate(listdir):
        path = os.path.join(baseDir, el)
        print(
            f"{Back.CYAN +
                Fore.BLACK}{centerChar(index)}{Back.RESET + Fore.RESET}: {path}"
        )

    try:
        selectedIndex = int(
            input(f"{Fore.GREEN}Select the index of the file:{Fore.RESET}\n"))

        if selectedIndex == -1:
            selection = parent
        else:
            selection = os.path.join(baseDir, listdir[selectedIndex])
        if not os.path.isfile(selection):
            selection = askPath(selection)

        return selection
    except IndexError:
        raise InvalidInput(
            f"Can't select the file {
                selectedIndex + 1}/{len(listdir)}"
        )
        return None
    except ValueError:
        print(
            f"{Fore.RED}Error, please select a valid integer number, please try again")
        return askPath(baseDir)

    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        return None


if __name__ == "__main__":
    baseDir = Config.read("Files", "data_dir")
    print(askPath(baseDir))
