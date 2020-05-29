import tkinter as tk
from frontend.Settings import *


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.bg = BACK_GROUND_COLOR

        # --------------------------------------------------toolbar--------------------------------------

        self.toolbar_frame = tk.Frame(master=self, height=70, width=WIDTH_WINDOW - 54,
                                      borderwidth=5, relief='groove', highlightbackground="black",
                                      highlightcolor="black",
                                      highlightthickness=1, bg=BACK_GROUND_COLOR).place(x=51, y=0)

        self.button_graphics_img = tk.PhotoImage(file='frontend/Widget/icons/graphic.png')
        self.button_graphic = tk.Button(master=self, text='Test/Train',
                                        image=self.button_graphics_img, height=25, width=25, bg=BACK_GROUND_COLOR,
                                        command=lambda: controller.show_frame("GraphicPage")).place(x=75, y=5)

        self.label_graphic = tk.Label(master=self, text='Plot Parameters',
                                      height=0, width=12, bg=BACK_GROUND_COLOR).place(x=55, y=40)
