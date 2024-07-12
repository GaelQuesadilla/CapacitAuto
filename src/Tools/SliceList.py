from .GetIndexes import getIndexes


def sliceList(element, *args):
    indexes = getIndexes(element, args)
    print(indexes)
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
