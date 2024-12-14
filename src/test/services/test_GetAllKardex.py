import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.Model.services.AllKardex import AllKardex
from src.Model.exceptions.invalid_curp_error import InvalidCurp


class TestAllKardex(unittest.TestCase):

    @patch('src.Config.Config.read', return_value="utf-8")
    def test_initialization(self, mock_config: MagicMock):
        kardex = AllKardex(fileName="test.json", curps=["ABC123", "XYZ789"])
        self.assertEqual(kardex.fileName, "test.json")
        self.assertEqual(kardex.curps, ["ABC123", "XYZ789"])
        self.assertEqual(kardex.allKardex, [])
        self.assertEqual(kardex.invalidCurps, [])

    @patch('src.Config.Config.read', return_value="path.json")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_saveAllKardex(self, mock_json_dump: MagicMock, mock_file: MagicMock, mock_config: MagicMock):
        # Preparar el objeto AllKardex con datos de prueba
        kardex = AllKardex(fileName="test.json")
        kardex._allKardex = [{"Name": "Test User", "Final_Grade": 95}]

        # Llamar al método que estamos probando
        kardex.saveAllKardex()

        # Verificar que se hizo una llamada a json.dump() con _allKardex
        mock_json_dump.assert_any_call(kardex._allKardex, mock_file())

    @patch("builtins.open", new_callable=mock_open)
    def test_saveReport(self, mock_file):
        kardex = AllKardex(fileName="test.json")
        kardex._invalidCurps = ["INVALID123", "INVALID456"]
        kardex.saveReport()

        mock_file.assert_called_once_with(
            "test_report.txt", "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_any_call("INVALID123\n")
        handle.write.assert_any_call("INVALID456\n")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"Name": "Test User", "Final_Grade": 95}]')
    @patch("json.load", return_value=[{"Name": "Test User", "Final_Grade": 95}])
    def test_loadAllKardex(self, mock_json_load, mock_file):
        kardex = AllKardex(fileName="test.json")
        kardex.loadAllKardex()

        mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")
        mock_json_load.assert_called_once_with(mock_file())
        self.assertEqual(
            kardex.allKardex, [
                {"Name": "Test User", "Final_Grade": 95}])

    @patch("src.Log.setup_logger")
    @patch("src.Model.services.ReadKardex.ReadKardex.getInfo")
    def test_requestAllKardex(self, mockReadKardex: MagicMock, mockSetup_logger):
        curps: list = ["VALID_CURP123", "INVALID_CURP123"]
        allKardex = AllKardex(curps=curps)
        allKardex.requestAllKardex()

        self.assertEqual(
            mockReadKardex.call_count, 2

        )


if __name__ == "__main__":
    unittest.main()
