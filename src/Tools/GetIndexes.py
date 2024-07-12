def getIndexes(element, *args):
    indexes = []
    for index, el in enumerate(element):
        if el in args[0]:
            indexes.append(index)

    if len(indexes) == 0:
        return -1

    return indexes


if __name__ == "__main__":
    pass
