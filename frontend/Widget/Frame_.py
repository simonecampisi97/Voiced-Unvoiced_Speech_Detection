import tkinter as tk


class Frame(tk.Frame):

    def __init__(self, window_root, x, y, height, width, borderwidth, relief, command=None):
        super().__init__(master=window_root, height=height, width=width, relief=relief,
                         borderwidth=borderwidth, command=command, bd=1)
        self.place(x=x, y=y)
        self.pack_propagate(False)
