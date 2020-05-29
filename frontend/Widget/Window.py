import tkinter as tk
from tkinter import ttk
from frontend.Widget import Label, Button, Frame_

BACK_GROUND_COLOR = '#D6DBDF'
WIDTH_WINDOW = 800
HEIGHT_WINDOW = 500


class Window(tk.Tk):

    def __init__(self, title, resizable):
        super().__init__()
        # -----------ROOT WINDOWS-------------
        self.title(title)
        self.hidden = 0
        self.resizable(resizable, resizable)
        self.geometry(str(WIDTH_WINDOW) + 'x' + str(HEIGHT_WINDOW))
        self.configure(bg=BACK_GROUND_COLOR)
        self.position = 0

        # ------------TOOLBAR------------------
        self.toolbar_frame = None
        self.button_graphic = None
        self.button_graphics_img = tk.PhotoImage(file='frontend/Widget/icons/graphic.png')
        self.label_graphic = None
        self.button_tool2 = None

        # --------------GRAPHIC FRAME --------------
        self.graphic_frame = None

        # ----------Menu Bar-------------------------

        self.menu_frame = Frame_.Frame(window_root=self, height=HEIGHT_WINDOW, width=50, x=65, y=0,
                                       borderwidth=5, relief='groove')

        self.menu_frame.configure(highlightbackground="black",
                                  highlightcolor="black", highlightthickness=1, bg=BACK_GROUND_COLOR)
        self.menu_frame.place(x=0)

        # Menu Button
        self.menu_img = tk.PhotoImage(file='frontend/Widget/icons/menu.png')
        self.menu_button = Button.Button(root_window=self.menu_frame, image=self.menu_img, height=25, width=25)
        self.menu_button.configure(bg=BACK_GROUND_COLOR)
        self.menu_button.bind('<Button-1>', self.show_frame_menu)
        self.menu_button.place(x=10, y=10)

        # Back Button
        self.back_img = tk.PhotoImage(file='frontend/Widget/icons/back.png')
        self.back_button = Button.Button(root_window=self.menu_frame, image=self.back_img, height=25, width=25)
        self.back_button.configure(bg=BACK_GROUND_COLOR)
        self.back_button.bind('<Button-1>', self.go_back)
        self.back_button.place(x=10, y=46)

        # Home Button
        self.home_img = tk.PhotoImage(file='frontend/Widget/icons/home.png')
        self.home_button = Button.Button(root_window=self.menu_frame, image=self.home_img, height=25, width=25)
        self.home_button.configure(bg=BACK_GROUND_COLOR)
        self.home_button.place(x=10, y=82)
        self.home_button.bind('<Button-1>', self.home_page)

    def show_frame_menu(self, event):
        self.toolbar_frame = Frame_.Frame(window_root=self, height=60, width=WIDTH_WINDOW - 54, x=51, y=0,
                                          borderwidth=5, relief='groove')
        self.toolbar_frame.configure(highlightbackground="black", highlightcolor="black",
                                     highlightthickness=1, bg=BACK_GROUND_COLOR)

        self.button_graphic = Button.Button(root_window=self.toolbar_frame, text='Test/Train',
                                            image=self.button_graphics_img, height=25, width=25,
                                            command=self.show_frame_graphics)
        self.button_graphic.configure(bg=BACK_GROUND_COLOR)
        self.button_graphic.place(x=55, y=5)
        self.label_graphic = Label.Label(window_root=self.toolbar_frame, text='Plot Parameters',
                                         x=15, y=30, height=0, width=15)
        self.label_graphic.configure(bg=BACK_GROUND_COLOR)

    def show_frame_graphics(self):
        self.graphic_frame = Frame_.Frame(window_root=self, height=HEIGHT_WINDOW - 54, width=WIDTH_WINDOW - 54, x=51,
                                          y=60,
                                          borderwidth=5, relief='groove')
        self.graphic_frame.configure(highlightbackground="black", highlightcolor="black",
                                     highlightthickness=1, bg=BACK_GROUND_COLOR)

    def changePage(self, change):
        pages = [self.pageOne, self.pageTwo, self.pageThree]
        new_position = self.position + change
        if (new_position < 0) or (new_position <= len(pages)):
            show_frame(BlankPage)
            # not sure how you would handle the new position here
        else:
            pages[new_position].tkraise()
            self.position = new_position

    def go_back(self, event):
        self.changePage(-1)

    def go_next(self, event):
        self.changePage(1)

    def home_page(self, event):
        if self.toolbar_frame is not None:
            self.toolbar_frame.destroy()
        self.graphic_frame.destroy()