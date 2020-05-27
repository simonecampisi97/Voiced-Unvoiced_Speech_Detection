import tkinter as tk


class Button(tk.Button):

    def __init__(self, root_window, x, y, text='', command=None, height=5, width=25):
        super().__init__(text=text, command=command, master=root_window, width=width, height=height)
        self.place(x=x, y=y)
