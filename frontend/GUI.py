import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont
from frontend.HomePage import HomePage
from frontend.GraphicPage import GraphicPage
from frontend.NeuralNetworkPage import NeuralNetworkPage
from frontend.Settings import *


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('VOICED/UNVOICED SPEECH DETECTION')
        self.resizable(RESIZABLE, RESIZABLE)
        self.geometry(str(WIDTH_WINDOW) + 'x' + str(HEIGHT_WINDOW))
        self.configure(bg=BACK_GROUND_COLOR)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.iconbitmap(default='frontend/icons/speech1.ico')
        # self.iconwindow(pathName=tk.PhotoImage('frontend/icons/speech1.ico'))

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, bg=BACK_GROUND_COLOR, borderwidth=0, highlightbackground="black",
                             highlightcolor="black", highlightthickness=1)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # --------------MENU BAR---------------------------

        self.menu_frame = tk.LabelFrame(master=self, height=HEIGHT_WINDOW, width=50,
                                        borderwidth=2, relief='flat', highlightbackground="black",
                                        highlightcolor="black", highlightthickness=1,
                                        bg=SIDE_BAR_COLOR).place(x=0, y=0)

        # Home Button
        self.home_img = tk.PhotoImage(file='frontend/icons/home.png')
        self.home_button = tk.Button(master=self.menu_frame, image=self.home_img, height=25, width=25,
                                     bg=SIDE_BAR_COLOR, command=self.go_home, activebackground=SIDE_BAR_COLOR,
                                     relief='flat')

        self.home_button.place(x=10, y=15)
        # Back Button
        self.back_img = tk.PhotoImage(file='frontend/icons/back.png')

        self.back_button = tk.Button(master=self.menu_frame, image=self.back_img, height=25, width=25,
                                     bg=SIDE_BAR_COLOR, relief='flat',
                                     command=lambda: self.show_frame("HomePage"), activebackground=SIDE_BAR_COLOR)
        self.back_button.place(x=10, y=56)
        s = ttk.Style()
        s.configure('TSeparator', foreground='black', background='black')
        self.separator = ttk.Separator(master=self.menu_frame, orient=tk.HORIZONTAL).place(x=0.3, y=100, relwidth=0.05)

        self.button_graphics_img = tk.PhotoImage(file='frontend/icons/graphic.png')
        self.button_graphic = tk.Button(master=self.menu_frame, relief='flat', activebackground=SIDE_BAR_COLOR,
                                        image=self.button_graphics_img, height=25, width=25, bg=MENU_COLOR,
                                        command=lambda: self.show_frame("GraphicPage")).place(x=10, y=120)

        self.neural_img = tk.PhotoImage(file='frontend/icons/neural.png')
        self.button_neural = tk.Button(master=self.menu_frame, relief='flat', activebackground=SIDE_BAR_COLOR,
                                       image=self.neural_img, height=25, width=25, bg=MENU_COLOR,
                                       command=lambda: self.show_frame("NeuralNetworkPage")).place(x=10, y=180)

        self.frames = {}
        for F in (HomePage, GraphicPage, NeuralNetworkPage):
            page_name = F.__name__
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

    def go_home(self):
        self.show_frame('HomePage')
