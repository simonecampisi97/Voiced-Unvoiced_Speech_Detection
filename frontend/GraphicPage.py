import tkinter as tk
from frontend.Settings import *


class GraphicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.graphic_frame = tk.Frame(master=self, height=HEIGHT_WINDOW - 54,
                                      width=WIDTH_WINDOW - 54, borderwidth=5, relief='groove', highlightbackground="black",
                                      highlightcolor="black", highlightthickness=1, bg=BACK_GROUND_COLOR).place( x=51,y=60)
