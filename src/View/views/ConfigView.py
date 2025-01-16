import tkinter as tk
from src.View.widgets.ConfigWidget import ConfigWidget
from src.Config import Config
import ttkbootstrap as ttk


class ConfigView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.title = ttk.Label(self, text="Configuración")
        self.title.pack(fill=ttk.X)

        self.configFile = Config.getPath("Files", "config_dir")
        if not self.configFile.is_file():
            Config.create()

        self.configWidget = ConfigWidget(self, configFile=self.configFile)
        self.configWidget.pack(expand=True, fill=ttk.BOTH)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = ConfigView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
