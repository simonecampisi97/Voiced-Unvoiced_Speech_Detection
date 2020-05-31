import tkinter as tk
from frontend.Settings import *
from frontend.HomePage import HomePage
from tkinter import font as tkfont


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.bg = BACK_GROUND_COLOR
        self.controller.back_button.configure(command=self.controller.go_home)

        self.font_label = self.title_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")

        # --------------------------------------------------toolbar--------------------------------------

        self.toolbar_frame_ = tk.LabelFrame(master=self, height=70, width=WIDTH_WINDOW - 51,
                                            borderwidth=2, relief='flat', highlightbackground="black",
                                            highlightcolor="black",
                                            highlightthickness=1, bg=MENU_COLOR).place(x=49, y=0)

        self.button_graphics_img = tk.PhotoImage(file='frontend/icons/graphic.png')
        self.button_graphic = tk.Button(master=self, relief='flat',
                                        image=self.button_graphics_img, height=25, width=25, bg=BACK_GROUND_COLOR,
                                        command=lambda: self.controller.show_frame("GraphicPage")).place(x=150, y=5)

        self.label_graphic = tk.Label(master=self, text='Plot',
                                      height=0, width=12,font=self.font_label,
                                      bg=MENU_COLOR).place(x=115, y=38)

        self.button_train_img = tk.PhotoImage(file='frontend/icons/train.png')
        self.button_train = tk.Button(master=self, text='Test/Train', relief='flat',
                                      image=self.button_train_img, height=25, width=25, bg=BACK_GROUND_COLOR,
                                      command=lambda: self.controller.show_frame("TrainTest")).place(x=250, y=5)

        self.label_train = tk.Label(master=self, text='Train/Test',
                                    height=0, width=12, bg=MENU_COLOR,
                                    font=self.font_label).place(x=215, y=38)
