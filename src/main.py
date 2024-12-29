import tkinter as tk
from src.View.components.BaseView import BaseView
from src.View.views.ConfigView import ConfigView
from src.Config import Config
from src.Log import setup_logger, trackFunction
import pathlib
import os

logger = setup_logger()

school_shift = Config.read("School", "school_shift")
school_key = Config.read("School", "school_key")


class MainApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("800x496")
        self.root.title(f"CAPACITAUTO COBACH {school_key} {school_shift}")

        self.isConfigOpen = False

        self.icon = tk.PhotoImage(file=Config.read("Assets", "logo_image_dir"))

        self.configFile = pathlib.Path(Config.read("Files", "config_dir"))

        if not self.configFile.is_file():
            Config.create()

        self.root.iconphoto(False, self.icon)

        self.base_view = BaseView(root)
        self.file_path = None

        self.config_button = tk.Button(
            root, text="Configuración",
            command=self.open_config_view
        )

        self.config_button.pack(pady=20)

    def open_config_view(self):
        config_view = ConfigView(
            self.root, self.configFile, self.on_config_saved)
        config_view.show()

    def on_config_saved(self):
        print("La configuración ha sido guardada y la aplicación está actualizada.")

    @trackFunction
    def show(self):
        self.base_view.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    app.show()
