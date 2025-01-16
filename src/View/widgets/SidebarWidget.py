import tkinter as tk
import ttkbootstrap as ttk
from typing import Dict, Callable, Union
from dataclasses import dataclass
from src.Log import setup_logger
from ttkbootstrap import constants as c

logger = setup_logger()


@dataclass
class currentWidget:
    name: str
    widget: tk.Widget


class SidebarWidget(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, style=c.DARK)

        self.configure(
            width=400,
            padding=[20, 30],

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
            command=lambda: onClick(),
            padding=[3, 10],
            style=c.DARK
        )
        button.pack(fill=ttk.X, expand=True)

        self.buttonData[name] = {"widget": widget, "button": button}

    def selectWidget(self, name):
        self.onClick(name)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    app = AppWindow()

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
