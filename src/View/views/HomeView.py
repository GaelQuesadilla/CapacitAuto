import tkinter as tk
import ttkbootstrap as ttk
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap import constants as c
from src.Controller.controllers.update import update
from src.Controller.controllers.deleteInfo import deleteInfo
from src.Controller.controllers.report import report
from src.Config import Config
from ttkbootstrap.dialogs import Messagebox
YES = ["yes", "Yes", "si", "sí", "Si", "Sí"]


class HomeView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.scrollable = ScrolledFrame(self)
        self.scrollable.pack(fill=ttk.BOTH, expand=True)
        self.header = ttk.Frame(self.scrollable)
        self.header.pack(fill=ttk.X)

        self.title = TitleLabel(self.header, text="Bienvenido a Capacitauto")
        self.title.pack(padx=10,
                        pady=20, fill=tk.X, expand=True)
        description = """
        Capacitauto es una herramienta diseñada para gestionar y organizar
        grupos escolares de forma eficiente. Con funcionalidades como el
        cálculo de promedios, organización de materias por grupo, y la
        creación de listas de estudiantes para capacitación y paquetes, Capacitauto facilita
        el trabajo administrativo en los planteles del COBACH BCS
        """
        self.description = ttk.Label(
            self.header, text=description, justify=tk.LEFT)
        self.description.pack(fill=tk.X, expand=True)

        self.optionFrame = ttk.Frame(self.scrollable)
        self.optionFrame.pack(fill=ttk.X)

        self.optionTitle = TitleLabel(self.optionFrame, text="Opciones")

        self.updateAppButton = ttk.Button(
            self.optionFrame, text="Instalar actualizaciones", padding=[10, 10],
            style=c.SUCCESS, command=self.updateApp)
        self.updateAppButton.pack(side=ttk.LEFT, padx=15)

        self.restoreConfigButton = ttk.Button(
            self.optionFrame, text="Restablecer configuración", padding=[10, 10],
            style=c.SECONDARY, command=self.restoreConfigApp)
        self.restoreConfigButton.pack(side=ttk.LEFT, padx=15)

        self.reportErrorButton = ttk.Button(
            self.optionFrame, text="Reportar error", padding=[10, 10],
            style=c.WARNING, command=self.reportError)
        self.reportErrorButton.pack(side=ttk.LEFT, padx=15)

        self.deleteDataButton = ttk.Button(
            self.optionFrame, text="Eliminar datos", padding=[10, 10],
            style=c.DANGER, command=self.deleteAppInfo)
        self.deleteDataButton.pack(side=ttk.LEFT, padx=15)

    def updateApp(self):
        yesnoQuestion = Messagebox.yesno(
            title="Actualizar aplicación",
            message="Se actualizará la aplicación, esto puede causar errores.\n"
            "Por favor, contacte al correo gaelglz032@gmail.com antes de continuar.\n"
            "¿Desea continuar?",
            alert=True
        )
        if yesnoQuestion in YES:
            deleteInfo()

    def deleteAppInfo(self):
        yesnoQuestion = Messagebox.yesno(
            title="Eliminar datos",
            message="Se eliminarán los datos de la aplicación, esta acción es irreversible.\n"
            "¿Desea continuar?",
            alert=True
        )
        if yesnoQuestion in YES:
            deleteInfo()

    def reportError(self):
        yesnoQuestion = Messagebox.yesno(
            title="Reportar error",
            message="A continuación se abrirá un correo electrónico, por favor describa el problema.\n"
            "¿Desea continuar?",
            alert=True
        )
        if yesnoQuestion in YES:
            report()

    def restoreConfigApp(self):
        yesnoQuestion = Messagebox.yesno(
            title="Restablecer configuración",
            message="Se restablecerán los ajustes, esta acción es irreversible.\n"
            "¿Desea continuar?",
            alert=True
        )
        if yesnoQuestion in YES:
            Config.create()
            Config.setup()


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = HomeView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
