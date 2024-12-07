def normalizeText(text: str) -> str:
    """Returns a value with no special characters, replacing them with an analogous character

    Parameters
    ----------
    text : str
        The string to normalize

    Returns
    -------
    str
        The normalized string
    """

    special_characters = {
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",
        "Ü": "U",
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ü": "u",
    }

    for character in special_characters:
        text = text.replace(character, special_characters.get(character))

    return text


if __name__ == "__main__":
    pass
