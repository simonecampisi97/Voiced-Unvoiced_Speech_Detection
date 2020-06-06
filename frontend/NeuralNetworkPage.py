import tkinter as tk
import tkinter.ttk as ttk
from frontend.Settings import *
import matplotlib.pyplot as plt
from frontend.GraphicPage import plot_on_tab, popup_message
from Net import Net
from utils.support_funcion import visualizeNN
from tkinter import font as tkfont


class NeuralNetworkPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bg = BACK_GROUND_COLOR

        self.nn = Net()

        try:
            self.nn.load_model()
            self.nn.load_weights()
        except FileNotFoundError:
            font_pop = tkfont.Font(family='arial black', size=20, weight="bold")
            popup_message('MODEL NOT FOUND!', font=font_pop)
            return
        self.nn.compile()

        self.frame_nn = tk.Frame(master=self, height=HEIGHT_WINDOW,
                                 width=WIDTH_WINDOW - 51)
        self.frame_nn.place(x=51, y=0)

        figure = plt.figure(figsize=(13, 8), dpi=73, tight_layout=True)

        ax = figure.add_subplot(111)
        visualizeNN(ax=ax, model=self.nn.model, input_shape=18)
        plot_on_tab(figure=figure, master=self.frame_nn)
