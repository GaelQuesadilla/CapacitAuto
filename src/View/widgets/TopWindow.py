import tkinter as tk
from tkinter import ttk
from src.Log import setup_logger
from src.Config import Config


logger = setup_logger(loggerName="ConfigView")


class TopWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("400x200")
        self.icon = tk.PhotoImage(file=Config.read("Assets", "logo_image_dir"))

        self.title("TopWindow")

        self.iconphoto(False, self.icon)


if __name__ == "__main__":

    parent = tk.Tk()
    topWindow = TopWindow(parent=parent)
    parent.mainloop()
