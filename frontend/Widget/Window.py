import tkinter as tk
from tkinter import ttk
from frontend.Widget import Label, Button, Frame_
from PIL import Image, ImageTk


class Window(tk.Tk):

    def __init__(self, title, geometry, resizable):
        super().__init__()
        self.title(title)
        self.hidden = 0
        self.resizable(resizable, resizable)
        self.geometry(geometry)
        self.toolbar = None
        self.button_tool1 = None
        self.button_tool1_img = tk.PhotoImage(file='frontend/Widget/icons/train.png')
        self.button_tool2 = None

        self.menu_img = tk.PhotoImage(file='frontend/Widget/icons/menu.png')
        self.menu_button = Button.Button(root_window=self, image=self.menu_img, height=64, width=64)
        self.menu_button.bind('<Button-1>', self.show_frame_menu)
        self.menu_button.place(x=2, y=2)

        self.back_img = tk.PhotoImage(file='frontend/Widget/icons/back.png')
        self.back_button = Button.Button(root_window=self, image=self.back_img, height=64, width=64)
        self.back_button.bind('<Destroy>', self.destroy_)
        self.back_button.place(x=2, y=66)

    def show_frame_menu(self, event):
        self.toolbar = Frame_.Frame(window_root=self, height=65, width=801, x=65, y=0,
                                    borderwidth=3, relief='groove')

        self.button_tool1 = Button.Button(root_window=self.toolbar, text='Test/Train', image=self.button_tool1_img,
                                          height=64,width=64)
        self.button_tool1.place(x=50, y=2)

    def destroy_(self, event):
        self.toolbar.destroy()
