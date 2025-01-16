from src.Config import Config
from src.View.widgets.AppWindow import AppWindow
from src.View.widgets.SidebarWidget import SidebarWidget
from src.View.views.CurpManagerView import CurpManagerView
from src.View.views.AllSubjectsView import AllSubjectsView
from src.View.views.ChoiceView import ChoiceView
from src.View.views.ConfigView import ConfigView
from src.View.views.ListsView import ListsView
from src.View.views.HomeView import HomeView
from src.View.views.ResultsView import ResultsView
from src.Log import setup_logger
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as ttk
logger = setup_logger()


class App(AppWindow):
    def __init__(self):
        super().__init__()
        self.geometry("1000x600")

        self.sidebar = SidebarWidget()
        self.sidebar.configure(width=200)
        self.sidebar.pack(side=ttk.LEFT, fill=ttk.Y)

        self.content = ttk.Frame(self)
        self.content.pack(expand=True, fill=ttk.BOTH)

        def curpManagerView(): return CurpManagerView(self.content)
        def homeView(): return HomeView(self.content)
        def allSubjectsView(): return AllSubjectsView(self.content)
        def listsView(): return ListsView(self.content)
        def configView(): return ConfigView(self.content)
        def choiceView(): return ChoiceView(self.content)
        def resultsView(): return ResultsView(self.content)

        self.sidebar.addButton("Inicio", homeView)
        self.sidebar.addButton("Administración de CURPS", curpManagerView)
        self.sidebar.addButton("Relación de materias", allSubjectsView)
        self.sidebar.addButton("Listas de alumnos", listsView)
        self.sidebar.addButton("Elecciones de grupo", choiceView)
        self.sidebar.addButton("Resultados", resultsView)
        self.sidebar.addButton("Configuración", configView)

        self.sidebar.selectWidget("Administración de CURPS")

    def destroy(self):
        logger.info("EXIT APP")
        return super().destroy()

    def mainloop(self, n=0):
        logger.info("START APP")

        try:
            super().mainloop(n)
        except Exception as e:
            logger.error(f"Error en la aplicación. Error : {e}")
            Messagebox.show_error(
                title="Error", message=f"Error en la aplicación : {e}"
            )


if __name__ == "__main__":

    app = App()
    app.mainloop()
