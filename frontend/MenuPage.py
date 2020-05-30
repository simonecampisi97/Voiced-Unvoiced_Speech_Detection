import tkinter as tk
from frontend.Settings import *
from frontend.HomePage import HomePage
from tkinter import font as tkfont


class MenuPage(HomePage):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.bg = BACK_GROUND_COLOR

        self.font_label = self.title_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")

        # -----------------MENU BAR---------------------
        self.menu_frame = tk.Frame(master=self, height=HEIGHT_WINDOW, width=50,
                                   borderwidth=2, relief='flat', highlightbackground="black",
                                   highlightcolor="black", highlightthickness=1, bg=BACK_GROUND_COLOR).place(x=0, y=0)

        # Back Button
        self.back_img = tk.PhotoImage(file='frontend/icons/back.png')
        self.back_button = tk.Button(master=self.menu_frame, image=self.back_img, height=25, width=25,
                                     bg=BACK_GROUND_COLOR, relief='flat',
                                     command=lambda: controller.show_frame("HomePage")).place(x=10, y=46)

        # --------------------------------------------------toolbar--------------------------------------

        self.toolbar_frame_ = tk.LabelFrame(master=self, height=70, width=WIDTH_WINDOW - 54,
                                            borderwidth=2, relief='flat', highlightbackground="black",
                                            highlightcolor="black",
                                            highlightthickness=1, bg=BACK_GROUND_COLOR).place(x=51, y=0)

        self.button_graphics_img = tk.PhotoImage(file='frontend/icons/graphic.png')
        self.button_graphic = tk.Button(master=self, relief='flat',
                                        image=self.button_graphics_img, height=25, width=25, bg=BACK_GROUND_COLOR,
                                        command=lambda: controller.show_frame("GraphicPage")).place(x=150, y=5)

        self.label_graphic = tk.Label(master=self, text='Plot',
                                      height=0, width=12, bg=BACK_GROUND_COLOR, font=self.font_label).place(x=115, y=38)

        self.button_train_img = tk.PhotoImage(file='frontend/icons/train.png')
        self.button_train = tk.Button(master=self, text='Test/Train', relief='flat',
                                      image=self.button_train_img, height=25, width=25, bg=BACK_GROUND_COLOR,
                                      command=lambda: controller.show_frame("TrainTest")).place(x=250, y=5)

        self.label_train = tk.Label(master=self, text='Train/Test',
                                    height=0, width=12, bg=BACK_GROUND_COLOR, font=self.font_label).place(x=215, y=38)