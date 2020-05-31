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
from Frames import Frames
from utils.utils import *
from ParametersExtraction import *

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def popup_message(msg):
    popup = tk.Tk()
    popup.resizable(RESIZABLE, RESIZABLE)
    popup.geometry('250x150')
    popup.wm_title("ERROR!")
    font = tkfont.Font(family='arial black', size=20, weight="bold")
    label = ttk.Label(popup, text=msg, font=font)
    label.pack(pady=20)
    B1 = ttk.Button(popup, text="exit", command=popup.destroy)
    B1.pack(side='bottom', pady=25)


def plot_on_tab(figure, master):
    canvas = FigureCanvasTkAgg(figure=figure, master=master)
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, master)
    toolbar.update()


def create_frame_plot(tab):
    frame = tk.Frame(master=tab, height=HEIGHT_WINDOW - 55,
                     width=WIDTH_WINDOW - 215)
    frame.place(x=0, y=0)
    return frame


def update_frame_plot(frame, tab):
    frame.destroy()
    frame_ = create_frame_plot(tab=tab)
    return frame_


class GraphicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.file_path = ""
        self.bg = BACK_GROUND_COLOR
        self.font_label = self.title_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")

        self.controller.back_button.configure(command=self.controller.go_menu)
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
        self.frame_plot = create_frame_plot(tab=self.tab_VUV)

        self.tab_zcr = ttk.Frame(self.tabControl)
        self.frame_plot2 = create_frame_plot(tab=self.tab_zcr)

        self.tab_mag = ttk.Frame(self.tabControl)

        self.tabControl.place(x=200, y=20)
        self.tabControl.add(self.tab_VUV, text='VUV')
        self.tabControl.add(self.tab_zcr, text='st-zcr')
        self.tabControl.add(self.tab_mag, text='st-magnitude')

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

    def plot_signal(self):
        self.frame_plot = update_frame_plot(self.frame_plot, tab=self.tab_VUV)
        self.frame_plot2 = update_frame_plot(self.frame_plot2, tab=self.tab_zcr)

        if self.file_path == "":
            popup_message("Upload The file first!")
            return

        # read wav file
        fs, y = wavfile.read(self.file_path)
        frames = Frames(fs=fs, y=y)
        # time axis (milliseconds)
        time = np.arange(len(y)) * 1000 * (1 / fs)

        figure = plt.Figure(figsize=(9, 5), dpi=90)
        ax = figure.add_subplot(111)
        ax.plot(time, y, ms=1)
        plot_on_tab(figure=figure, master=self.frame_plot)

        figure2 = plt.Figure(figsize=(9, 5), dpi=90)
        ax2 = figure2.add_subplot(111)
        zcr = st_zcr(frames)
        plot_result(signal=zcr, Frames=frames, ax=ax2)
        plot_on_tab(figure=figure2, master=self.frame_plot2)
