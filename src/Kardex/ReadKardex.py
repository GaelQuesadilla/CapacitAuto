from bs4 import BeautifulSoup


def clean(soup: list):
    cleanSoup = []

    for line in soup:
        cleanLine = line

        cleanLine = cleanLine.replace("\xa0", " ")
        cleanLine = cleanLine.replace("\u200e", " ")
        cleanLine = cleanLine.replace(" ", " ")

        for _ in range(10):

            newCleanLine = cleanLine.replace("  ", " ")
            if cleanLine == newCleanLine:
                break
            cleanLine = newCleanLine

        if cleanLine == "":
            continue
        if cleanLine == " ":
            continue

        cleanSoup.append(cleanLine)
    return cleanSoup


def readKardex(kardex):
    soup = BeautifulSoup(kardex.content, "html.parser")
    cleanSoup = clean(soup.get_text().splitlines())
    print(cleanSoup)


if __name__ == "__main__":
    from .GetStudentKardex import GetStudentKardex
    kardex = GetStudentKardex("GOMG060722HBSNNLA5")
    readKardex(kardex)
