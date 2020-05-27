import tkinter as tk
from frontend.Widget import Label, Button, Frame_


class Window(tk.Tk):

    def __init__(self, title, geometry, resizable):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(resizable, resizable)

        self.train_test_button = Button.Button(root_window=self, text='Train/Test', x=0, y=0, height=10, width=25)

        self.Graphics = Button.Button(root_window=self, text='Graphic Given \n a signal', x=170, y=0, height=10, width=25)
