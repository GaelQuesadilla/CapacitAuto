import tkinter as tk
import ttkbootstrap as ttk
from src.View.MainApp import MainApp
from typing import Dict, Callable, Union
from dataclasses import dataclass
from src.Log import setup_logger

logger = setup_logger()


@dataclass
class currentWidget:
    name: str
    widget: tk.Widget


class SidebarWidget(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.configure(
            width=300,
            relief="sunken",
            padding=[20, 10]
        )

        self.buttonData: Dict[str, Dict[str, Union[Callable, ttk.Button]]] = {}

        self.currentWidget: currentWidget = currentWidget(None, None)

    def onClick(self, name: str):

        if self.currentWidget.name == name:
            return
        if not self.currentWidget.widget is None:
            self.currentWidget.widget.destroy()

        newWidget = self.buttonData.get(name).get("widget", None)()
        self.currentWidget = currentWidget(name, newWidget)

        logger.info(f"Loading '{name}' Widget as view")
        self.currentWidget.widget.pack(fill=ttk.BOTH, expand=True)

    def addButton(self, name: str, widget: Callable, onClick=None):

        if onClick is None:
            def onClick(): return self.onClick(name)

        button = ttk.Button(
            self,
            text=name,
            command=lambda: onClick()
        )
        button.pack(fill=ttk.X, pady=3, padx=20)

        self.buttonData[name] = {"widget": widget, "button": button}

    def selectWidget(self, name):
        self.onClick(name)


if __name__ == "__main__":

    app = MainApp()

    sidebar = SidebarWidget(app)
    sidebar.pack(side=ttk.LEFT, fill=ttk.Y)
    i = 0

    def primary(): return ttk.Frame(app, style=ttk.PRIMARY)
    def secondary(): return ttk.Frame(app, style=ttk.SECONDARY)
    def warning(): return ttk.Frame(app, style=ttk.WARNING)

    sidebar.addButton("primary", primary)
    sidebar.addButton("secondary", secondary)
    sidebar.addButton("warning", warning)

    app.mainloop()
