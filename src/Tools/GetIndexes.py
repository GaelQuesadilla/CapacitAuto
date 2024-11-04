from typing import List


def getIndexes(element: list | str, *args) -> List[int]:
    """Get the indexes of the specified element in a list or string

    Parameters
    ----------
    element : list or str
        The element on which the search will be done

    Args
    ----------
    params : list or str
        The element to search

    Returns
    -------
    list
        A list that contains the indexes of the the specified elements in element
    """
    indexes = []
    for index, el in enumerate(element):
        if el in args[0]:
            indexes.append(index)

    if len(indexes) == 0:
        return -1

    return indexes


if __name__ == "__main__":
    pass
