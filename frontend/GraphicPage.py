import tkinter as tk
import tkinter.ttk as ttk
from frontend.Settings import *
from tkinter import font as tkfont
from tkinter import filedialog
import matplotlib.pyplot as plt
from Frames import Frames
import librosa
import matplotlib
from Net import Net
import ParametersExtraction as pe
from utils.support_funcion import plot_result, plot_model_prediction
import utils.model_evaluation as me

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

DATASET_DIR_SIMO = "C:\\Users\\simoc\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"
DATASET_DIR_ALE = "C:\\Users\\carot\\Documents\\SPEECH_DATA_ZIPPED\\SPEECH DATA"




def popup_message(msg, font, w=250, h=150):
    popup = tk.Tk()
    popup.resizable(RESIZABLE, RESIZABLE)
    popup.configure(bg=BACK_GROUND_COLOR)
    popup.geometry(str(w) + 'x' + str(h))
    popup.wm_title("ERROR!")

    label = tk.Label(master=popup, text=msg, font=font, bg=BACK_GROUND_COLOR)
    label.pack(pady=20)
    B1 = ttk.Button(popup, text="exit", command=popup.destroy)
    B1.pack(side='bottom', pady=25)


def plot_on_tab(figure, master):
    canvas = FigureCanvasTkAgg(figure=figure, master=master)
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, master)
    toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
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
        self.folder_path = ""
        self.message_select_folder = tk.Message(master=self, relief='groove', width=100, bg=BACK_GROUND_COLOR)
        self.message_select_folder.place(x=70, y=350)
        self.gender = None

        self.message_select_audio = tk.Message(master=self, relief='groove', width=100, bg=BACK_GROUND_COLOR)
        self.message_select_audio.place(x=70, y=75)
        self.bg = BACK_GROUND_COLOR
        self.font_label = self.title_font = tkfont.Font(family='Helvetica', size=10, weight="bold", slant="italic")
        self.font = tkfont.Font(family='Helvetica', size=7)
        self.font_pop = tkfont.Font(family='arial black', size=20, weight="bold")

        self.nn = Net()

        try:
            self.nn.load_model()
            self.nn.load_weights()
        except FileNotFoundError:
            popup_message('MODEL NOT FOUND!', font=self.font_pop)
            return
        self.nn.compile()

        self.controller.back_button.configure(command=self.controller.go_menu)
        # --------------------------------------------------------------------------------------------------

        self.upload_frame = tk.LabelFrame(master=self, text='Upload File Audio', font=self.font_label, height=150,
                                          width=130, borderwidth=2, relief='flat', highlightbackground="black",
                                          highlightcolor="black", highlightthickness=1,
                                          bg=BACK_GROUND_COLOR).place(x=60, y=20)

        self.upload_button = tk.Button(master=self, text='File Explorer',
                                       height=1, width=10, relief='groove', activebackground=BACK_GROUND_COLOR,
                                       bg=BACK_GROUND_COLOR, command=self.upload_file_audio).place(x=80, y=45)

        self.label_male = tk.Label(master=self, text='Male', bg=BACK_GROUND_COLOR).place(x=80, y=100)
        self.label_female = tk.Label(master=self, text='Female', bg=BACK_GROUND_COLOR).place(x=125, y=100)

        s = ttk.Style()
        s.configure('TRadiobutton', background=BACK_GROUND_COLOR)

        self.radio_button_male = ttk.Radiobutton(master=self, command=self.select_male, value=1).place(x=85, y=120)
        self.radio_button_female = ttk.Radiobutton(master=self, compound='top',
                                                   command=self.select_female, value=2).place(x=132, y=122)

        self.plot_button = tk.Button(master=self, text='Plot', activebackground=BACK_GROUND_COLOR,
                                     height=1, width=10, relief='groove',
                                     bg=BACK_GROUND_COLOR, command=self.plot_signal).place(x=80, y=180)

        self.model_evaluation_frame = tk.LabelFrame(master=self, text='Model Evaluation', font=self.font_label,
                                                    height=200,
                                                    width=130, borderwidth=2, relief='flat',
                                                    highlightbackground="black",
                                                    highlightcolor="black", highlightthickness=1,
                                                    bg=BACK_GROUND_COLOR).place(x=60, y=250)

        self.label_choose_folder = tk.Label(master=self, text='Choose Test Folder:',
                                            bg=BACK_GROUND_COLOR).place(x=67, y=275)
        self.upload_button_acc = tk.Button(master=self, text='File Explorer',
                                           height=1, width=10, relief='groove', activebackground=BACK_GROUND_COLOR,
                                           bg=BACK_GROUND_COLOR, command=self.select_folder).place(x=80, y=300)

        self.evaluate_button = tk.Button(master=self, text='Evaluate', activebackground=BACK_GROUND_COLOR,
                                         height=1, width=10, relief='groove',
                                         bg=BACK_GROUND_COLOR,
                                         command=self.evaluate_model).place(x=80, y=460)

        self.tabControl = ttk.Notebook(master=self, height=HEIGHT_WINDOW - 50, width=WIDTH_WINDOW - 210)

        self.tab_VUV = ttk.Frame(self.tabControl)
        self.frame_plot = create_frame_plot(tab=self.tab_VUV)

        self.tab_zcr = ttk.Frame(self.tabControl)
        self.frame_plot2 = create_frame_plot(tab=self.tab_zcr)

        self.tab_mag = ttk.Frame(self.tabControl)
        self.frame_plot3 = create_frame_plot(tab=self.tab_mag)

        self.tab_hnr = ttk.Frame(self.tabControl)
        self.frame_plot4 = create_frame_plot(tab=self.tab_hnr)

        self.tab_energy = ttk.Frame(self.tabControl)
        self.frame_plot5 = create_frame_plot(tab=self.tab_energy)

        self.tabControl.place(x=200, y=20)
        self.tabControl.add(self.tab_VUV, text='VUV')
        self.tabControl.add(self.tab_zcr, text='st-zcr')
        self.tabControl.add(self.tab_mag, text='st-magnitude')
        self.tabControl.add(self.tab_hnr, text='st-hnr')
        self.tabControl.add(self.tab_energy, text='st-energy')

    def select_male(self):
        self.gender = 1

    def select_female(self):
        self.gender = 0

    def upload_file_audio(self):
        self.file_path = filedialog.askopenfilename(title="Select Audio File",
                                                    filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
        var = tk.StringVar()
        self.message_select_audio.destroy()
        self.message_select_audio = tk.Message(master=self, relief='groove', width=100,
                                               textvariable=var, font=self.font)
        self.message_select_audio.place(x=70, y=75)
        var.set(str(self.file_path).split('/')[-1])

    def select_folder(self):

        self.folder_path = filedialog.askdirectory(title="Choose Test Directory")

        var = tk.StringVar()
        label = tk.Label(master=self, text='Data Folder:', bg=BACK_GROUND_COLOR).place(x=70, y=330)
        self.message_select_folder.destroy()
        self.message_select_folder = tk.Message(master=self, relief='groove', width=100,
                                                textvariable=var, font=self.font)
        self.message_select_folder.place(x=70, y=350)
        var.set(str(self.folder_path).split('/')[-1])


    def evaluate_model(self):

        font_eval = tkfont.Font(family='Calibre', size=9, weight='bold')
        font_not_found = tkfont.Font(family='Calibre', size=5, weight='bold')

        if self.folder_path == "":
            popup_message("Select a test folder first!", font=self.font_pop)
            return
        self.folder_path = self.folder_path.replace('/', '\\')

        try:

            ds, file_num, frame_num = me.load_evaluation_data(self.folder_path)
        except FileNotFoundError as err:
            error = str(err).split(':', 1)
            popup_message(error[0] + ':\n\n\n' + error[1], font=font_not_found, h=200, w=400)
            return

        accuracy, loss = me.evaluate_model(self.nn.model, ds)

        accuracy = round(accuracy * 100, 2)
        loss = round(loss, 2)

        label_accuracy = tk.Label(master=self, text='ACCURACY: ' + str(accuracy) + '%',
                                  bg=BACK_GROUND_COLOR, font=font_eval).place(x=66, y=380)
        loss_label = tk.Label(master=self, text='LOSS: ' + str(loss),
                              bg=BACK_GROUND_COLOR, font=font_eval).place(x=66, y=410)

    def plot_signal(self):
        self.frame_plot = update_frame_plot(self.frame_plot, tab=self.tab_VUV)
        self.frame_plot2 = update_frame_plot(self.frame_plot2, tab=self.tab_zcr)
        self.frame_plot3 = update_frame_plot(self.frame_plot3, tab=self.tab_mag)
        self.frame_plot4 = update_frame_plot(self.frame_plot4, tab=self.tab_hnr)
        self.frame_plot5 = update_frame_plot(self.frame_plot5, tab=self.tab_energy)

        if self.file_path == "":
            popup_message("Upload The file first!", font=self.font_pop)
            return
        if self.gender is None:
            popup_message("Select the gender first!", font=self.font_pop)
            return

        # read wav file
        y, fs = librosa.load(self.file_path)
        frames = Frames(fs=fs, y=y)
        # time axis (milliseconds)
        print(self.gender)
        try:
            figure = plot_model_prediction(path_file=self.file_path, model=self.nn.model, gender=self.gender,
                                           data_root=DATASET_DIR_ALE)
        except (FileNotFoundError, IndexError):
            try:
                figure = plot_model_prediction(path_file=self.file_path, model=self.nn.model, gender=self.gender,
                                               data_root=DATASET_DIR_SIMO)
            except (FileNotFoundError, IndexError):
                figure = plot_model_prediction(path_file=self.file_path, model=self.nn.model, gender=self.gender)

        plot_on_tab(figure=figure, master=self.frame_plot)

        figure2 = plt.Figure(figsize=(9, 5), dpi=90)
        ax2 = figure2.add_subplot(111)
        ax2.set_title('Short-Time Zero Crossing Rate', fontsize=20)
        ax2.set_xlabel('frame_time')
        ax2.set_ylabel('zcr')
        zcr = pe.st_zcr(frames)
        plot_result(signal=zcr, Frames=frames, ax=ax2)
        plot_on_tab(figure=figure2, master=self.frame_plot2)

        figure3 = plt.Figure(figsize=(9, 5), dpi=90)
        ax3 = figure3.add_subplot(111)
        ax3.set_title('Short-Time Magnitude', fontsize=20)
        ax3.set_xlabel('frame_time')
        ax3.set_ylabel('magnitude')
        mag = pe.st_magnitude(frames)
        plot_result(signal=mag, Frames=frames, ax=ax3)
        plot_on_tab(figure=figure3, master=self.frame_plot3)

        figure4 = plt.Figure(figsize=(9, 5), dpi=90)
        ax4 = figure4.add_subplot(111)
        ax4.set_title('Short-Time Harmonic-To-Noise Ratio', fontsize=20)
        ax4.set_xlabel('frame_time')
        ax4.set_ylabel('hnr')
        hnr = pe.st_HNR(frames)
        plot_result(signal=hnr, Frames=frames, ax=ax4)
        plot_on_tab(figure=figure4, master=self.frame_plot4)

        figure5 = plt.Figure(figsize=(9, 5), dpi=90)
        ax5 = figure5.add_subplot(111)
        ax5.set_title('Short-Time Energy', fontsize=20)
        ax5.set_xlabel('frame_time')
        ax5.set_ylabel('energy')
        energy = pe.st_energy(frames)
        plot_result(signal=energy, Frames=frames, ax=ax5)
        plot_on_tab(figure=figure5, master=self.frame_plot5)
