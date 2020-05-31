import tkinter as tk
from frontend.Settings import *
from frontend.HomePage import HomePage


class TrainTest(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = BACK_GROUND_COLOR
        self.controller.back_button.configure(command=self.controller.go_menu)

        label = tk.Label(self, text="Train/Test PAGE", font=controller.title_font, bg=BACK_GROUND_COLOR)
        label.pack(side="top", fill="x", pady=10)
