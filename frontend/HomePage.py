import tkinter as tk
from frontend.Settings import *


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = BACK_GROUND_COLOR
        #self.controller.back_button.configure(command=lambda: self.controller.show_frame('HomePage'))
        label = tk.Label(self, text="HOME PAGE", font=self.controller.title_font, bg=BACK_GROUND_COLOR)
        label.pack(side="top", fill="x", pady=10)


