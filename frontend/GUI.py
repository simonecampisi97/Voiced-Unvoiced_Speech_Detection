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
        container = tk.Frame(self, bg=BACK_GROUND_COLOR, borderwidth=0, highlightbackground="black",
                             highlightcolor="black", highlightthickness=1)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # --------------MENU BAR---------------------------

        hp = HomePage(parent=container, controller=self)

        self.frames = {}
        for F in (HomePage, MenuPage, GraphicPage):
            page_name = F.__name__
            if page_name != "HomePage":
                frame = F(parent=container, controller=self, home_page=hp)
            else:
                frame = F(parent=container, controller=self)

            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg=BACK_GROUND_COLOR)

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
