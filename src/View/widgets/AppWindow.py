from src.Log import setup_logger, trackFunction
from src.Config import Config
import tkinter as tk

logger = setup_logger(loggerName=__name__)

school_shift = Config.read("School", "school_shift")
school_key = Config.read("School", "school_key")


class AppWindow(tk.Tk):
    def __init__(self, screenName=None, baseName=None, className="Tk", useTk=True, sync=False, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.geometry("800x496")
        self.title(f"CAPACITAUTO COBACH {school_key} {school_shift}")

        self.icon = tk.PhotoImage(file=Config.read("Assets", "logo_image_dir"))
        self.iconphoto(False, self.icon)


if __name__ == "__main__":
    view = AppWindow()
    view.mainloop()
