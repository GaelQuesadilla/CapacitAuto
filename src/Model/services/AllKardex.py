from src.Model.services.ReadKardex import ReadKardex
from src.Model.exceptions.invalid_curp_error import InvalidCurp
import json
from src.Config import Config
from src.Log import setup_logger, trackFunction
from typing import List, Dict, Any


logging = setup_logger()


encoding = Config.read("General", "encoding")


class AllKardex():
    def __init__(self, fileName: str = None,  curps: List[str] = None):
        self.fileName: str = fileName
        self.curps: List[str] = curps
        self._invalidCurps: List[str] = []
        self._allKardex: List[Dict[str: Any]] = []

    def saveAllKardex(self):
        with open(self.fileName, "w", encoding=encoding) as file:
            json.dump(self._allKardex, file)

        self.kardexData = {
            "invalidCurps": self.invalidCurps,
            "availableGroups": list(set([student.get("Group") for student in self.allKardex])),
            "availableShifts": list(set([student.get("Shift") for student in self.allKardex])),
            "availableSemesters": list(set([student.get("Semester") for student in self.allKardex])),
        }
        with open(Config.read("Files", "kardex_data_dir"), "w", encoding=encoding) as file:
            json.dump(self.kardexData, file)

    def saveReport(self):
        with open(self.fileName.replace(".json", "_report.txt"), "w", encoding=encoding) as file:
            for curp in self.invalidCurps:
                file.write(f"{curp}\n")

    def loadAllKardex(self):
        with open(self.fileName, "r", encoding=encoding) as file:
            logging.info(f"Kardex cargado desde {self.fileName}")
            self._allKardex = json.load(file)

    @trackFunction
    def requestAllKardex(self):
        for curp in self.curps:
            curp = curp.replace("\n", "")
            current = ReadKardex(curp)
            try:
                info = current.getInfo()
                logging.info(
                    f"{curp}: {info.get('Name')}, {info.get('Semester')}, {
                        info.get('Group')}, {info.get("Final_Grade")}"
                )
                self._allKardex.append(info)
            except InvalidCurp:
                logging.warning(
                    f"{curp}: CURP NO VALIDA"
                )
                self._invalidCurps.append(curp)

    @property
    def allKardex(self):
        return self._allKardex

    @property
    def invalidCurps(self):
        return self._invalidCurps


if __name__ == "__main__":
    import os
    curps = open(os.path.join(Config.read(
        "Files", "data_dir"), "CURPS.txt")).read()

    allKardex = AllKardex(os.path.join(Config.read(
        "Files", "data_dir"), "AllKardex.json"), curps.splitlines())

    allKardex.requestAllKardex()

    allKardex.saveAllKardex()
    allKardex.saveReport()
