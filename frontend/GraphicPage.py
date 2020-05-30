import tkinter as tk
from frontend.Settings import *
from frontend.HomePage import HomePage
from tkinter import font as tkfont
from tkinter import filedialog


class GraphicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = BACK_GROUND_COLOR
        self.font_label = self.title_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")

        # ------------------------------MENU BAR-------------------------------------------------------

        self.menu_frame = tk.LabelFrame(master=self, height=HEIGHT_WINDOW, width=50,
                                        borderwidth=2, relief='flat', highlightbackground="black",
                                        highlightcolor="black", highlightthickness=1, bg=BACK_GROUND_COLOR).place(x=0,
                                                                                                                  y=0)

        self.menu_img = tk.PhotoImage(file='frontend/icons/menu.png')
        self.menu_button = tk.Button(master=self.menu_frame, image=self.menu_img,
                                     height=25, width=25, relief='flat',
                                     command=lambda: controller.show_frame("MenuPage"),
                                     bg=BACK_GROUND_COLOR).place(x=10, y=10)

        # Back Button
        self.back_img = tk.PhotoImage(file='frontend/icons/back.png')
        self.back_button = tk.Button(master=self.menu_frame, image=self.back_img, height=25, width=25,
                                     bg=BACK_GROUND_COLOR, relief='flat',
                                     command=lambda: controller.show_frame("MenuPage")).place(x=10, y=46)

        # --------------------------------------------------------------------------------------------------

        self.upload_frame = tk.LabelFrame(master=self, text='Upload File Audio', font=self.font_label, height=80,
                                          width=130, borderwidth=2, relief='flat', highlightbackground="black",
                                          highlightcolor="black", highlightthickness=1,
                                          bg=BACK_GROUND_COLOR).place(x=80, y=20)

        self.upload_button = tk.Button(master=self, text='File Explorer',
                                       height=1, width=10, relief='groove',
                                       bg=BACK_GROUND_COLOR, command=self.upload_file).place(x=100, y=45)

    #

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        textFile = tk.Message(master=self, relief='groove').place(x=100, y=65)
