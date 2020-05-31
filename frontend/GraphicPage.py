import tkinter as tk
from frontend.Settings import *
from frontend.HomePage import HomePage
from tkinter import font as tkfont
import tkinter.ttk as ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib
from scipy.io import wavfile
import numpy as np

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class GraphicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.file_path = ""
        self.bg = BACK_GROUND_COLOR
        self.font_label = self.title_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")

        # --------------------------------------------------------------------------------------------------

        self.upload_frame = tk.LabelFrame(master=self, text='Upload File Audio', font=self.font_label, height=150,
                                          width=130, borderwidth=2, relief='flat', highlightbackground="black",
                                          highlightcolor="black", highlightthickness=1,
                                          bg=BACK_GROUND_COLOR).place(x=60, y=20)

        self.upload_button = tk.Button(master=self, text='File Explorer',
                                       height=1, width=10, relief='groove',
                                       bg=BACK_GROUND_COLOR, command=self.upload_file).place(x=80, y=45)

        self.tabControl = ttk.Notebook(master=self, height=HEIGHT_WINDOW - 50,
                                       width=WIDTH_WINDOW - 210)

        self.tab_VUV = ttk.Frame(self.tabControl)
        self.frame_plot = self.create_frame_plot()

        self.tab_plot2 = ttk.Frame(self.tabControl)
        self.tab_plot3 = ttk.Frame(self.tabControl)
        self.tabControl.place(x=200, y=20)
        self.tabControl.add(self.tab_VUV, text='VUV')
        self.tabControl.add(self.tab_plot2, text='plot2')
        self.tabControl.add(self.tab_plot3, text='plot3')

        self.plot_button = tk.Button(master=self, text='Plot',
                                     height=1, width=10, relief='groove',
                                     bg=BACK_GROUND_COLOR, command=self.plot_signal).place(x=80, y=180)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Select Audio File",
                                                    filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
        font = tkfont.Font(family='Helvetica', size=7)
        var = tk.StringVar()
        text_label = tk.Message(master=self, relief='groove', width=100,
                                textvariable=var, font=font).place(x=70, y=75)
        var.set(str(self.file_path).split('/')[-1])

    def create_frame_plot(self):
        frame = tk.Frame(master=self.tab_VUV, height=HEIGHT_WINDOW - 50,
                         width=WIDTH_WINDOW - 210, highlightbackground="black",
                         highlightcolor="black", highlightthickness=1, borderwidth=5)
        frame.place(x=0, y=0)
        return frame

    def update_frame_plot(self, frame):
        frame.destroy()
        frame_ = self.create_frame_plot()
        return frame_

    def plot_signal(self):
        self.frame_plot = self.update_frame_plot(self.frame_plot)

        print(self.file_path)
        if self.file_path == "":
            self.popup_msg("Upload The file first!")
            return
        fs, y = wavfile.read(self.file_path)
        time = np.arange(len(y)) * 1000 * (1 / fs)
        figure = plt.Figure(figsize=(6, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(time, y)
        chart_type = FigureCanvasTkAgg(figure=figure, master=self.frame_plot)
        chart_type.get_tk_widget().pack()

    def popup_msg(self, msg):
        popup = tk.Tk()
        popup.resizable(RESIZABLE, RESIZABLE)
        popup.wm_title("ERROR!")
        font = tkfont.Font(family='Helvetica', size=20, weight="bold")
        label = ttk.Label(popup, text=msg, font=font)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="exit", command=popup.destroy)
        B1.pack()
