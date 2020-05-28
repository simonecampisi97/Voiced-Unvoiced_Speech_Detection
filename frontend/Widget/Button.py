import tkinter as tk


class Button(tk.Button):

    def __init__(self, root_window, text=None, command=None, height=5, width=5, path_img=None, image=None):
        super().__init__(text=text, command=command, master=root_window,
                         width=width, height=height, borderwidth=0, image=image)

        if path_img is not None:
            img = tk.PhotoImage(file=path_img)
            img.subsample(5,5)
            self.config(image=img)
