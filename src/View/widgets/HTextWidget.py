import ttkbootstrap as ttk
from ttkbootstrap import constants as c
from ttkbootstrap.scrolled import ScrolledFrame


class TextWM():

    def AddTitle(self, title, font_size=18, font_weight="bold"):

        title_label = ttk.Label(
            self, text=title, font=(font_weight, font_size),
            style=c.PRIMARY)
        title_label.pack(anchor=ttk.W, padx=10, pady=5)

    def AddSubtitle(self, subtitle, font_size=14, font_weight="normal"):

        subtitle_label = ttk.Label(
            self, text=subtitle, font=(font_weight, font_size),
            style=c.SECONDARY)
        subtitle_label.pack(anchor=ttk.W, padx=10, pady=3)

    def AddText(self, text, font_size=12):

        text_label = ttk.Label(
            self, text=text, wraplength=500, font=(font_size,))
        text_label.pack(anchor=ttk.W, padx=10, pady=5)

    def AddBulletList(self, items, font_size=12):

        for item in items:
            list_item_label = ttk.Label(
                self, text=f"- {item}",  wraplength=500, font=(font_size,))
            list_item_label.pack(anchor=ttk.W, padx=10, pady=3)

    def AddEnumList(self, items, font_size=12):

        for index, item in enumerate(items):
            list_item_label = ttk.Label(
                self, text=f"{index+1}. {item}",  wraplength=500, font=(font_size,))
            list_item_label.pack(anchor=ttk.W, padx=10, pady=3)


class HTextWidget(ttk.Frame, TextWM):
    pass


class ScrollableHTextWidget(ScrolledFrame, TextWM):
    def __init__(self, master, autohide=True, *args, **kwargs):
        super().__init__(master, autohide, *args, **kwargs)


if __name__ == "__main__":
    from src.View.widgets.AppWindow import AppWindow

    view = AppWindow()

    component = ScrollableHTextWidget(view)
    component.pack(expand=True, fill=ttk.BOTH)
    component.AddTitle("Titulo")
    component.AddSubtitle("Subtitulo")
    component.AddText(
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    )
    component.AddBulletList([
        "Elemento 1",
        "Elemento 2",
        "Elemento 3",
        "Elemento 4",
        "Elemento 5",
    ])
    component.AddEnumList([
        "Elemento 1",
        "Elemento 2",
        "Elemento 3",
        "Elemento 4",
        "Elemento 5",
    ])

    view.mainloop()
