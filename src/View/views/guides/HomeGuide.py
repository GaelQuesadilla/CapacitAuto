from src.View.widgets.HTextWidget import ScrollableHTextWidget
import ttkbootstrap as ttk


class HomeGuide(ScrollableHTextWidget):
    def __init__(self, master, autohide=True, *args, **kwargs):
        super().__init__(master, autohide, *args, **kwargs)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow
    app = AppWindow()
    component = HomeGuide(app)
    component.pack(fill=ttk.BOTH, expand=True)

    app.mainloop()
