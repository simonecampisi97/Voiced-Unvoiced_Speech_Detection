import tkinter as tk


class Label(tk.Label):

    def __init__(self, window_root, text, x, y, ):
        super().__init__(text=text, master=window_root)
        self.place(x=x, y=y)
