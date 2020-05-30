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

        # --------------------------------------------------------------------------------------------------

        self.upload_frame = tk.LabelFrame(master=self, text='Upload File Audio', font=self.font_label, height=100,
                                          width=130, borderwidth=2, relief='flat', highlightbackground="black",
                                          highlightcolor="black", highlightthickness=1,
                                          bg=BACK_GROUND_COLOR).place(x=80, y=20)

        self.upload_button = tk.Button(master=self, text='File Explorer',
                                       height=1, width=10, relief='groove',
                                       bg=BACK_GROUND_COLOR, command=self.upload_file).place(x=100, y=45)

    #

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        var = tk.StringVar()
        textFile = tk.Message(master=self, relief='groove', width=50, textvariable=var).place(x=100, y=75)
        var.set(str(file_path).split('/')[-1])
