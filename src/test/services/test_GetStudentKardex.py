from src.Model.services.GetStudentKardex import GetStudentKardex
from unittest import TestCase
from src.Config import Config
from bs4 import BeautifulSoup


class test_Student(TestCase):

    emptyKardexText: str = "No se encontró la información solicitada"

    def test_emptyKardex(self):
        response = GetStudentKardex("NOT VALID CURP 010101")
        soup = BeautifulSoup(response.content, "html.parser")

        self.assertTrue(soup.get_text().find(self.emptyKardexText) != -1)
