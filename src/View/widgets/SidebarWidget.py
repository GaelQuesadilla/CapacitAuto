import tkinter as tk
from src.View.MainApp import MainApp
from typing import Dict, Callable, Union, List
from dataclasses import dataclass
from src.Log import setup_logger

logger = setup_logger()


@dataclass
class currentWidget:
    name: str
    widget: tk.Widget


class SidebarWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.configure(
            width=300, bg="#2c3e50",
            relief="sunken", padx=20, pady=10
        )

        self.buttonData: Dict[str, Dict[str, Union[Callable, tk.Button]]] = {}

        self.currentWidget: currentWidget = currentWidget(None, None)

    def onClick(self, name: str):

        if self.currentWidget.name == name:
            return
        if not self.currentWidget.widget is None:
            self.currentWidget.widget.destroy()

        newWidget = self.buttonData.get(name).get("widget", None)()
        self.currentWidget = currentWidget(name, newWidget)

        logger.info(f"Loading '{name}' Widget as view")
        self.currentWidget.widget.pack(fill=tk.BOTH, expand=True)

    def addButton(self, name: str, widget: Callable, onClick=None):

        if onClick is None:
            def onClick(): return self.onClick(name)

        button = tk.Button(
            self,
            text=name,
            bg="#34495e",
            fg="white",
            relief=tk.FLAT,
            command=lambda: onClick()
        )
        button.pack(fill=tk.X, pady=3, padx=20)

        self.buttonData[name] = {"widget": widget, "button": button}

    def selectWidget(self, name):
        self.onClick(name)


if __name__ == "__main__":

    app = MainApp()

    sidebar = SidebarWidget(app)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    i = 0

    def red(): return tk.Frame(app, bg="red")
    def blue(): return tk.Frame(app, bg="blue")
    def purple(): return tk.Frame(app, bg="purple")

    sidebar.addButton("red", red)
    sidebar.addButton("blue", blue)
    sidebar.addButton("purple", purple)

    app.mainloop()
