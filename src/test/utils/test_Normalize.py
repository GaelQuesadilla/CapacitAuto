from src.utils.Normalize import normalizeText
from unittest import TestCase


class test_Normalize(TestCase):
    def test_accentCase(self):

        mock = "ÁáÉéÍíÓóÚú"
        ans = normalizeText(mock)
        self.assertTrue(ans == "AaEeIiOoUu")

    def test_emptyCase(self):
        mock = ""
        ans = normalizeText(mock)
        self.assertTrue(ans == "")

    def test_normalCase(self):
        mock = "AaEeIiOoUu"
        ans = normalizeText(mock)
        self.assertTrue(ans == mock)
