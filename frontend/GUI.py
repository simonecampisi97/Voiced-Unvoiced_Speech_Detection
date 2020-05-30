import tkinter as tk
from tkinter import font as tkfont
from frontend.HomePage import HomePage
from frontend.GraphicPage import GraphicPage
from frontend.MenuPage import MenuPage
from frontend.Settings import *


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('VOICED/UNVOICED SPEECH DETECTION')
        self.resizable(RESIZABLE, RESIZABLE)
        self.geometry(str(WIDTH_WINDOW) + 'x' + str(HEIGHT_WINDOW))
        self.configure(bg=BACK_GROUND_COLOR)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.menu_frame = tk.Frame(master=self, height=HEIGHT_WINDOW, width=50,
                                   borderwidth=5, relief='groove', highlightbackground="black",
                                   highlightcolor="black", highlightthickness=1, bg=BACK_GROUND_COLOR).place(x=0, y=0)
        # Menu Button
        self.menu_img = tk.PhotoImage(file='frontend/Widget/icons/menu.png')
        self.menu_button = tk.Button(master=self.menu_frame, image=self.menu_img,
                                     height=25, width=25,
                                     command=lambda: controller.show_frame("MenuPage"),
                                     bg=BACK_GROUND_COLOR).place(x=10, y=10)

        # Back Button
        self.back_img = tk.PhotoImage(file='frontend/Widget/icons/back.png')
        self.back_button = tk.Button(master=self.menu_frame, image=self.back_img, height=25, width=25,
                                     bg=BACK_GROUND_COLOR).place(x=10, y=46)

        # Home Button
        self.home_img = tk.PhotoImage(file='frontend/Widget/icons/home.png')
        self.home_button = tk.Button(master=self.menu_frame, image=self.home_img, height=25, width=25,
                                     bg=BACK_GROUND_COLOR).place(x=10, y=82)

        self.frames = {}
        for F in (MenuPage, GraphicPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        #self.show_frame("HomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
