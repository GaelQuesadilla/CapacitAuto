import tkinter as tk


class HomeView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.title = tk.Label(self, text="Bienvenido")
        self.title.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    window = AppWindow()

    view = HomeView(window)
    view.pack(fill=tk.BOTH, expand=True)

    window.mainloop()
