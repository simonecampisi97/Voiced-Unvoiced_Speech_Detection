import tkinter as tk
from frontend.Settings import *


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = BACK_GROUND_COLOR
        self.controller.back_button.configure(command=self.controller.go_home)
        self.logo = tk.PhotoImage(file='frontend/icons/speech_home.png')
        self.label_logo = tk.Label(image=self.logo, master=self, bg=BACK_GROUND_COLOR, height=75, width=75)
        self.label_logo.place(x=60, y=40)
        label = tk.Label(self, text="Voiced / Unvoiced Speech Detection", font=self.controller.title_font, bg=BACK_GROUND_COLOR)
        label.pack(side="top", fill="x", pady=10)
