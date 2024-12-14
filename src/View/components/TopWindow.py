import tkinter as tk
from tkinter import ttk
from src.Log import setup_logger
from src.Config import Config


logger = setup_logger(loggerName="ConfigView")


class TopWindow:

    def __init__(self, parent: tk.Tk):
        self._window: tk.Toplevel = None
        self.parent = parent

    @property
    def window(self):
        return self._window

    def show(self):
        self._window = tk.Toplevel(self.parent)

        self._window.geometry("400x200")
        self.icon = tk.PhotoImage(file=Config.read("Assets", "logo_image_dir"))

        self._window.title("TopWindow")

        self._window.iconphoto(False, self.icon)


if __name__ == "__main__":

    parent = tk.Tk()
    topWindow = TopWindow(parent=parent)
    topWindow.show()
    parent.mainloop()
