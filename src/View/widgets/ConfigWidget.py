import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from src.Config import default_config, Config
from configparser import ConfigParser
from typing import Dict, Any
from src.Log import setup_logger, trackFunction
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap import constants as c


logger = setup_logger(loggerName=__name__)


class ConfigWidget(ttk.Frame):
    def __init__(self, parent: tk.Widget, configFile: str):
        super().__init__(parent)

        self.parent = parent
        self.configFile = configFile
        self.config = ConfigParser()
        self.config.read(configFile)

        self.entriesBySection: Dict[str, Dict[str, ttk.Entry]] = {}

        self.save_button = ttk.Button(
            self, text="Guardar Configuración", command=self.saveConfig,
            style=c.PRIMARY
        )
        self.save_button.pack(fill=tk.X)

        self.scrollable = ScrolledFrame(self, autohide=True)
        self.scrollable.pack(fill=tk.BOTH, expand=True, pady=10)

        self.createConfigFields()

    def createConfigFields(self):
        for sectionName, sectionKeys in default_config.items():
            sectionFrame = self.createSectionFrame(sectionName)
            sectionFrame.pack(fill=ttk.X, padx=20, pady=3, expand=True)

            self.entriesBySection[sectionName] = {}
            for key, defaultValue in sectionKeys.items():

                frame = ttk.Frame(sectionFrame, padding=[5, 5])
                frame.pack(fill=ttk.X, expand=True)
                label = ttk.Label(
                    frame, text=key, padding=[10, 0],
                    font=("bold", 11))
                label.pack(fill=tk.X, side=tk.LEFT)

                value: Any = self.config.get(sectionName, key)
                entry = ttk.Entry(frame, width=200)
                entry.insert(0, value)
                entry.pack(side=tk.RIGHT)
                self.entriesBySection[sectionName][key] = entry

    def createSectionFrame(self, sectionName: str) -> ttk.Label:
        frame = ttk.LabelFrame(
            self.scrollable,
            text=sectionName, padding=[10, 10], style=c.SECONDARY)
        return frame

    def saveConfig(self):
        logger.info("Guardando configuración")

        try:

            for section, options in self.entriesBySection.items():
                for option, entry in options.items():
                    prev: str = self.config.get(section, option)
                    if entry.get() != prev:
                        logger.info(
                            f"Actualizando {section}.{option} de "
                            f"'{prev}' a '{entry.get()}'"
                        )
                    # Get entries
                    self.config.set(
                        section=section,
                        option=option,
                        value=entry.get())

            with open(self.configFile, "w") as file:
                self.config.write(file)

        except Exception as e:
            errorWindow = Messagebox.show_error(
                title="Error", message="No fue posible guardar la configuración")

            logger.error("No fue posible guardar la configuración")
            logger.error(e)


if __name__ == "__main__":

    from src.View.widgets.AppWindow import AppWindow

    configFile = Config.getPath("Files", "config_dir")

    if not configFile.is_file():
        Config.create()

    view = AppWindow()

    component = ConfigWidget(view, configFile)

    component.pack(fill=ttk.BOTH)

    view.mainloop()
