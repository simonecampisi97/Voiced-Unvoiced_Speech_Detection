import tkinter as tk
from frontend.Settings import *
from frontend.HomePage import *


class GraphicPage(tk.Frame):
    def __init__(self, parent, controller, home_page):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.home_page = home_page
        self.bg = BACK_GROUND_COLOR

        label = tk.Label(self, text="GRAPHIC PAGE", font=controller.title_font, bg=BACK_GROUND_COLOR)
        label.pack(side="top", fill="x", pady=10)

        # ------------------------------MENU BAR-------------------------------------------------------

        #home_page.back_button.bind('<Button-1>', lambda: controller.show_frame("MenuPage"))

        self.menu_frame = tk.Frame(master=self, height=HEIGHT_WINDOW, width=50,
                                   borderwidth=2, relief='flat', highlightbackground="black",
                                   highlightcolor="black", highlightthickness=1, bg=BACK_GROUND_COLOR).place(x=0, y=0)

        self.menu_img = tk.PhotoImage(file='frontend/icons/menu.png')
        self.menu_button = tk.Button(master=self, image=self.menu_img,
                                     height=25, width=25, relief='flat',
                                     command=lambda: controller.show_frame("MenuPage"),
                                     bg=BACK_GROUND_COLOR).place(x=10, y=10)

        # Back Button
        self.back_img = tk.PhotoImage(file='frontend/icons/back.png')
        self.back_button = tk.Button(master=self.menu_frame, image=self.back_img, height=25, width=25,
                                     bg=BACK_GROUND_COLOR, relief='flat',
                                     command=lambda: controller.show_frame("MenuPage")).place(x=10, y=46)

        # Home Button
        self.home_img = tk.PhotoImage(file='frontend/icons/home.png')
        self.home_button = tk.Button(master=self.menu_frame, image=self.home_img, height=25, width=25,
                                     bg=BACK_GROUND_COLOR, relief='flat',
                                     command=lambda: controller.show_frame("HomePage")).place(x=10, y=82)
