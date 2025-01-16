from src.Log import setup_logger
from src.Config import Config
import tkinter as tk
import ttkbootstrap as ttk

logger = setup_logger(loggerName=__name__)

school_shift = Config.read("School", "school_shift")
school_key = Config.read("School", "school_key")


class AppWindow(ttk.Window):
    def __init__(
            self,
            title=f"CAPACITAUTO COBACH {school_key} {school_shift}",
            themename="minty",
            iconphoto=Config.getPath("Assets", "logo_image_dir"),
            size=[800, 496],
            position=None,
            minsize=None,
            maxsize=None,
            resizable=None,
            hdpi=True,
            scaling=None,
            transient=None,
            overrideredirect=False,
            alpha=1
    ):

        super().__init__(
            title,
            themename,
            iconphoto,
            size,
            position,
            minsize,
            maxsize,
            resizable,
            hdpi,
            scaling,
            transient,
            overrideredirect,
            alpha
        )


if __name__ == "__main__":
    view = AppWindow()
    view.mainloop()
