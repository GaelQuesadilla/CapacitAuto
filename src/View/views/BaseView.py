import tkinter as tk


class BaseView:
    def __init__(self, root: tk.Tk):
        self.root = root

    def show(self):
        self.root.mainloop()
