import tkinter as tk
from frontend.Widget import Label, Button, Frame_


class Window(tk.Tk):

    def __init__(self, title, geometry, resizable):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(resizable, resizable)

        self.train_test_button = Button.Button(root_window=self, text='Train_Test', x=0, y=0)
