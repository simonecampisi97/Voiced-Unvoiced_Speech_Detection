import tkinter as tk
from frontend.Settings import *
from frontend.HomePage import HomePage
from tkinter import font as tkfont
import tkinter.ttk as ttk
from tkinter import filedialog
import matplotlib

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
                                       bg=BACK_GROUND_COLOR, command=self.upload_file).place(x=100, y=45)
        '''
        self.label_graphics = ttk.Tab(master=self, text='Plot signal', font=self.font_label,
                                           height=HEIGHT_WINDOW - 50,
                                            width=WIDTH_WINDOW - 210, borderwidth=2, relief='flat',
                                            highlightbackground="black",
                                            highlightcolor="black", highlightthickness=1,
                                            bg=BACK_GROUND_COLOR).place(x=200, y=20)
        # self.radio_button_VUV = tk.Radiobutton(self, text='VUV', command=self.plot_signal).place(x=230, y=45)
        '''
        self.tabControl = ttk.Notebook(master=self, height=HEIGHT_WINDOW - 50,
                                       width=WIDTH_WINDOW - 210)
        self.tab_VUV = ttk.Frame(self.tabControl)
        self.tab_plot2 = ttk.Frame(self.tabControl)
        self.tab_plot3 = ttk.Frame(self.tabControl)
        self.tabControl.place(x=200, y=20)
        self.tabControl.add(self.tab_VUV, text='VUV')
        self.tabControl.add(self.tab_plot2, text='plot2')
        self.tabControl.add(self.tab_plot3, text='plot3')

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Select Audio File",
                                                    filetypes=(("wav files", "*.wav"), ("all files", "*.*")))

        var = tk.StringVar()
        text_label = tk.Message(master=self, relief='groove', width=100,
                                textvariable=var).place(x=90, y=75)
        var.set(str(self.file_path).split('/')[-1])

    def plot_signal(self):
        print(self.file_path)
        if self.file_path == "":
            self.popup_msg("Upload The file first!")
            return
        # f = Figure(figsize=(5, 5), dpi=100)
        #a = f.add_subplot(111)
        #a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
        canvas = FigureCanvasTkAgg(master=self.tabControl)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas.draw_idle()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def popup_msg(self, msg):
        popup = tk.Tk()
        popup.resizable(RESIZABLE, RESIZABLE)
        popup.wm_title("ERROR!")
        font = tkfont.Font(family='Helvetica', size=20, weight="bold")
        label = ttk.Label(popup, text=msg, font=font)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="exit", command=popup.destroy)
        B1.pack()
