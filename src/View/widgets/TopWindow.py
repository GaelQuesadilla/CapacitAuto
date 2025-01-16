import ttkbootstrap as ttk
from src.Log import setup_logger
from src.Config import Config
from ttkbootstrap.window import Toplevel


logger = setup_logger(loggerName="ConfigView")


class TopWindow(Toplevel):
    def __init__(
            self,
            title="Nueva ventana",
            iconphoto=Config.getPath("Assets", "logo_image_dir"),
            size=[400, 200],
            position=None,
            minsize=None,
            maxsize=None,
            resizable=None,
            transient=None,
            overrideredirect=False,
            windowtype=None,
            topmost=False,
            toolwindow=False,
            alpha=1,
            **kwargs
    ):
        super().__init__(
            title,
            iconphoto,
            size,
            position,
            minsize,
            maxsize,
            resizable,
            transient,
            overrideredirect,
            windowtype,
            topmost,
            toolwindow,
            alpha,
            **kwargs
        )


if __name__ == "__main__":

    parent = ttk.Window(themename="minty")
    topWindow = TopWindow(parent)
    parent.mainloop()
