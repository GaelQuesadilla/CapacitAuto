import tkinter as tk
import ttkbootstrap as ttk


class HomeView(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.title = ttk.Label(self, text="Bienvenido")
        self.title.pack(fill=ttk.BOTH, expand=True)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = HomeView(window)
    view.pack(fill=ttk.BOTH, expand=True)

    window.mainloop()
