from .GetIndexes import getIndexes


def sliceList(element: list, *args) -> list:
    """Slice a list at the indexes where a specified element is located

    Parameters
    ----------
    element : list
        The element that will be sliced

    Args
    ----------
    params: str

    Returns
    -------
    list
        A list that contains the main element, sliced where args params were found
    """
    indexes = getIndexes(element, args)
    newElement = []

    previousIndex = 0
    for index in indexes:
        newSlice = element[previousIndex:index]
        previousIndex = index
        if len(newSlice) == 0:
            continue
        newElement.append(newSlice)

    newElement.append(element[previousIndex::])

    return newElement


if __name__ == "__main__":
    pass
