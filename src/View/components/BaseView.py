from src.Log import setup_logger, trackFunction
from src.Config import Config
import tkinter as tk

logger = setup_logger()

school_shift = Config.read("School", "school_shift")
school_key = Config.read("School", "school_key")


class BaseView:
    def __init__(self):
        self._root = tk.Tk()

        self._root.geometry("800x496")
        self._root.title(f"CAPACITAUTO COBACH {school_key} {school_shift}")

        self.icon = tk.PhotoImage(file=Config.read("Assets", "logo_image_dir"))
        self._root.iconphoto(False, self.icon)

    @trackFunction
    def show(self):
        self._root.mainloop()

    @property
    def root(self):
        return self._root


if __name__ == "__main__":
    view = BaseView()
    view.show()
