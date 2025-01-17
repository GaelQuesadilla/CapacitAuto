import tkinter as tk
import ttkbootstrap as ttk
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap import constants as c
from src.Controller.controllers.update import update


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
            style=c.SECONDARY)
        self.restoreConfigButton.pack(side=ttk.LEFT, padx=15)
        self.reportErrorButton = ttk.Button(
            self.optionFrame, text="Reportar error", padding=[10, 10],
            style=c.WARNING)
        self.reportErrorButton.pack(side=ttk.LEFT, padx=15)

        self.deleteDataButton = ttk.Button(
            self.optionFrame, text="Eliminar datos", padding=[10, 10],
            style=c.DANGER)
        self.deleteDataButton.pack(side=ttk.LEFT, padx=15)

    def updateApp(self):
        update()


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = HomeView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
