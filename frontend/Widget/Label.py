import tkinter as tk


class Label(tk.Label):

    def __init__(self, window_root, text, x, y, height, width):
        super().__init__(text=text, master=window_root, height=height, width=width, borderwidth=2)
        self.place(x=x, y=y)
