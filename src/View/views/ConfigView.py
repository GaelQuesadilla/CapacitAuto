import tkinter as tk
from src.View.widgets.ConfigWidget import ConfigWidget
from src.Config import Config
import ttkbootstrap as ttk
from src.View.widgets.Labels import TitleLabel
from src.View.widgets.Buttons import InfoButton


class ConfigView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.header = ttk.Frame(self)
        self.header.pack(fill=ttk.X)

        self.title = TitleLabel(self.header, text="Configuración")
        self.title.pack(side=ttk.LEFT)

        self.help = InfoButton(self.header)
        self.help.pack(side=ttk.RIGHT)

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
