import os


def getListDirs(baseDirectory: str, prefix: str = "*", suffix: str = "*"):
    """
    Get a list of directories and files, sorted and filtered by prefix and suffix.

    Parameters
    ----------
    baseDirectory : str
        The base directory to list the contents from.
    prefix : str, optional
        The prefix to filter files by. Files must start with this prefix to be included.
        Defaults to "*", which includes all files regardless of prefix.
    suffix : str, optional
        The suffix to filter files by. Files must end with this suffix to be included.
        Defaults to "*", which includes all files regardless of suffix.

    Returns
    -------
    list
        A sorted list of directories and files in the base directory, filtered by the given prefix and suffix.
    """
    allElements = os.listdir(baseDirectory)
    directories = []
    files = []

    for elementPath in allElements:
        path = os.path.join(baseDirectory, elementPath)

        if os.path.isdir(path):
            directories.append(elementPath)

        if os.path.isfile(path):

            hasPrefix = prefix == "*" or elementPath.startswith(prefix)
            hasSuffix = suffix == "*" or elementPath.endswith(suffix)

            if hasPrefix and hasSuffix:
                files.append(elementPath)

    directories.sort()
    files.sort()

    sorted_list = directories+files

    return sorted_list
