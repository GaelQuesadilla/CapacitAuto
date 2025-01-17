import tkinter as tk
import ttkbootstrap as ttk
from typing import Callable
import threading
from src.View.widgets.TopWindow import TopWindow


class ProgressWindow(TopWindow):
    def __init__(self, master=None, title=None):
        super().__init__(master)
        self.title(title)
        self.geometry("300x75")
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        self.progressBar = ttk.Progressbar(self, mode="indeterminate")
        self.progressBar.pack(fill=ttk.BOTH, expand=True, pady=20, padx=10)

    def start(self):
        self.progressBar.start()

    def stop(self):
        self.progressBar.stop()
        self.destroy()


def ProgressTask(parent: tk.Tk, title: str, onComplete: Callable = None):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):

            progressWindow = ProgressWindow(parent, title)
            progressWindow.start()

            def task():
                try:
                    func(*args, **kwargs)
                finally:
                    progressWindow.stop()
                    if onComplete:
                        onComplete()

            threading.Thread(target=task, daemon=True).start()

        return wrapper
    return decorator
