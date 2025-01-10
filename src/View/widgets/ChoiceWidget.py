from src.View.widgets.DataframeWidget import DataframeWidget
from src.View.widgets.AppWindow import AppWindow
import tkinter as tk
from src.Config import Config
from src.Model.services.CreateChoicesList import createChoicesList
from src.Log import setup_logger

logger = setup_logger()


class ChoiceWidget(DataframeWidget):

    def __init__(self, master):
        choicesPath = Config.getPath("Files", "choices_dir")
        super().__init__(master, fileName=choicesPath)

    def _createButtons(self):
        super()._createButtons()

        genButton = tk.Button(
            self.optionFrame, text="Generar archivo", command=self.generateNewChoicesExcel
        )

        genButton.pack(side=tk.LEFT, padx=10)

    def generateNewChoicesExcel(self):

        createChoicesList()
        self.loadDataFrame()
        self._createComponent()

    def _createComponent(self):
        super()._createComponent()
        try:

            self.tree.column("Semestre", width=50)
            self.tree.column("Grupo", width=50)
            self.tree.column("Turno", width=50)
        except tk.TclError:
            logger.warning("No es posible modificar el ancho de las columnas")


if __name__ == "__main__":
    from src.Config import Config

    view = AppWindow()
    component = ChoiceWidget(view)
    component.pack(fill=tk.BOTH, expand=True)

    view.mainloop()
