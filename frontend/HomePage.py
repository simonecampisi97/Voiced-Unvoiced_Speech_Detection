import tkinter as tk
from frontend.Settings import *
from tkinter import font as tkfont


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.font = tkfont.Font(family='Arial', size=18, weight="bold", slant='italic')
        self.controller = controller
        self.bg = BACK_GROUND_COLOR
        self.controller.back_button.configure(command=self.controller.go_home)
        self.logo = tk.PhotoImage(file='frontend/icons/speech_home.png')
        self.label_logo = tk.Label(image=self.logo, master=self, bg=BACK_GROUND_COLOR, height=75, width=75)
        self.label_logo.place(x=60, y=40)
        self.label_title = tk.Label(self, text="Voiced / Unvoiced Speech Detection \n With Neural Network",
                                    font=self.controller.title_font, bg=BACK_GROUND_COLOR)

        self.label_title.place(x=300, y=10)
        self.label_nome1 = tk.Label(master=self, bg=BACK_GROUND_COLOR, text='Simone Campisi', font=self.font)
        self.label_nome1.place(x=250, y=500)

        self.nn_img = tk.PhotoImage(file='frontend/icons/nn.png')
        self.nn = tk.Label(image=self.nn_img, master=self, bg=BACK_GROUND_COLOR)
        self.nn.place(x=300, y=80)

        self.label_nome2 = tk.Label(master=self, bg=BACK_GROUND_COLOR, text='Alessandro Caroti', font=self.font)
        self.label_nome2.place(x=550, y=500)
