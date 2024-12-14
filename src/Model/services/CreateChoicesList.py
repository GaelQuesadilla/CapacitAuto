from src.Model.models.DataList import DataList
from src.Model.services.AllKardex import AllKardex
import pandas as pd
from src.Config import Config


def createChoicesList():
    allKardex = AllKardex(fileName=Config.read("Files", "all_kardex_dir"))
    allKardex.loadAllKardex()

    data = [{
        "CURP": student.get("CURP"),
        "Semestre": student.get("Semester"),
        "Grupo": student.get("Group"),
        "Turno": student.get("Shift"),
        "Nombre": student.get("Name"),
    }
        for student in allKardex.allKardex
    ]

    df = pd.DataFrame(data)

    choicePrefix: str = Config.read("General", "choice_name")
    packages = Config.read("School", "packages").split(",")
    trainings = Config.read("School", "trainings").split(",")

    for choice in packages + trainings:
        df[choicePrefix.format(choice)] = ""

    dataList = DataList(fileName=Config.read("Files", "choices_dir"), df=df)
    dataList.sort(
        by=["Semestre", "Grupo", "Turno", "CURP", "Nombre"], ascending=True
    )

    dataList.save()

    print(df)


if __name__ == "__main__":
    createChoicesList()
