import tkinter as tk
from src.View.MainApp import MainApp


class SidebarWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.configure(
            width=400, bg="#2c3e50",
            relief="sunken", padx=20, pady=10
        )

        self.buttons = ["Home", "Settings", "Profile", "Help", "Exit"]
        for button_name in self.buttons:
            button = tk.Button(
                self,
                text=button_name,
                bg="#34495e",
                fg="white",
                relief="flat",
                command=lambda name=button_name: self.on_button_click(name)
            )
            button.pack(fill="x", pady=5, padx=10)

    def on_button_click(self, button_name):
        print(f"{button_name} button clicked")


if __name__ == "__main__":
    app = MainApp()
    sidebar = SidebarWidget(app)

    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    app.mainloop()
