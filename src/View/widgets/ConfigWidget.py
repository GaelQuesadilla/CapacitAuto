import tkinter as tk
from tkinter import ttk, messagebox
from src.Config import default_config, Config
from configparser import ConfigParser
from typing import Dict, Any, Callable
from src.Log import setup_logger, trackFunction
from src.View.widgets.TopWindow import TopWindow
import pathlib


logger = setup_logger(loggerName="ConfigView")


class ConfigWidget(tk.Frame):
    def __init__(self, parent: tk.Tk, configFile: str, onSaveConfig: Callable):
        self.parent = parent
        self.onSaveConfig = onSaveConfig
        self.configFile = configFile
        self.config = ConfigParser()
        self.config.read(configFile)

        self.entriesBySection: Dict[str, Dict[str, tk.Entry]] = {}

        super().__init__(parent)

    def createConfigFields(self):
        row = 1
        for sectionName, sectionKeys in default_config.items():
            sectionFrame = self.createSectionFrame(sectionName)
            sectionFrame.grid(row=row, column=0, padx=5, pady=3, sticky="ew")
            row += 1

            self.entriesBySection[sectionName] = {}
            for key, defaultValue in sectionKeys.items():
                label = ttk.Label(sectionFrame, text=key)
                label.grid(row=row, column=0, columnspan=2, padx=3, pady=3)

                value: Any = self.config.get(sectionName, key)
                entry = ttk.Entry(sectionFrame, width=60)
                entry.insert(0, value)
                entry.grid(row=row, column=2, columnspan=5)
                self.entriesBySection[sectionName][key] = entry
                row += 1

    def createSectionFrame(self, sectionName: str) -> tk.Tk:
        frame = ttk.LabelFrame(self.mainFrame, text=sectionName, padding=10)
        frame.columnconfigure(1, weight=10)
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
            errorWindow = messagebox.showerror(
                "Error", "No fue posible guardar la configuración")

            logger.error("No fue posible guardar la configuración")
            logger.error(e)

    @trackFunction
    def show(self):
        super()

        # Center main frame in column 1
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=1, column=1, sticky="nsew")

        self.scrollBar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.scrollBar.grid(row=1, column=3, sticky="ns")

        # Create a frame inside the canvas
        self.mainFrame = ttk.Frame(self.canvas, padding=10)
        self.canvas.create_window((0, 0), window=self.mainFrame, anchor="nw")

        # Configure scrollbar to control canvas scrolling
        self.canvas.configure(yscrollcommand=self.scrollBar.set)

        # Create the save button
        self.save_button = tk.Button(
            self, text="Guardar Configuración", command=self.saveConfig, bg="green"
        )
        self.save_button.grid(column=1, row=0, pady=10)

        self.createConfigFields()

        # Update canvas scroll region after all content is created
        self.mainFrame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":

    from src.View.widgets.AppWindow import AppWindow

    configFile = Config.getPath("Files", "config_dir")

    if not configFile.is_file():
        Config.create()

    def on_config_saved(self):
        print("Configuración guardada y aplicación actualizada.")

    view = AppWindow()

    component = ConfigWidget(view, configFile, on_config_saved)

    component.show()
    component.pack(fill=tk.BOTH)

    view.mainloop()
