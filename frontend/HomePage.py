import tkinter as tk
from frontend.Settings import *


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = BACK_GROUND_COLOR

        label = tk.Label(self, text="HOME PAGE", font=self.controller.title_font, bg=BACK_GROUND_COLOR)
        label.pack(side="top", fill="x", pady=10)

        # ----------Menu Bar-------------------------

        self.menu_frame = tk.LabelFrame(master=self, height=HEIGHT_WINDOW, width=50,
                                        borderwidth=2, relief='flat', highlightbackground="black",
                                        highlightcolor="black", highlightthickness=1, bg=BACK_GROUND_COLOR).place(x=0,
                                                                                                                  y=0)

        # Menu Button
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
