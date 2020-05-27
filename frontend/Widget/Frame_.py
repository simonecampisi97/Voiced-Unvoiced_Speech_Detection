import tkinter as tk


class Frame(tk.Frame):

    def __init__(self, window_root, text, x, y, ):
        super().__init__(text=text, master=window_root)
        self.place(x=x, y=y)
