import tkinter as tk
from tkinter import ttk
from typing import Callable
import threading


def ProgressTask(parent: tk.Tk, title: str, onComplete: Callable = None):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):

            progressBarWindow = tk.Toplevel(parent)
            progressBarWindow.title(title)
            progressBarWindow.geometry("300x50")

            progressBarWindow.protocol("WM_DELETE_WINDOW", lambda: None)

            progressBar = ttk.Progressbar(
                progressBarWindow, mode="indeterminate")
            progressBar.pack(fill=tk.BOTH, expand=True, pady=20, padx=10)
            progressBar.start()

            def task():
                try:
                    func(*args, **kwargs)
                finally:
                    progressBar.stop()
                    progressBarWindow.destroy()
                    if onComplete:
                        onComplete()

            threading.Thread(target=task, daemon=True).start()

        return wrapper
    return decorator
