import tkinter as tk
from src.View.widgets.AllSubjectsWidget import AllSubjectsWidget


class AllSubjectsView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.title = tk.Label(self, text="Relación de materias")
        self.title.pack(fill=tk.X)
        self.allSubjectsWidget = AllSubjectsWidget(self)
        self.allSubjectsWidget.pack(expand=True, fill=tk.BOTH)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = AllSubjectsView(window)
    view.pack(fill=tk.BOTH, expand=True)

    window.mainloop()
