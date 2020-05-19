import tkinter as tk
import tkinter.ttk as ttk

window_root = tk.Tk()
window_root.style = ttk.Style()
window_root.geometry("800x300")
window_root.title('Voiced/Unvoiced-speech detection')
window_root.style.theme_use('winnative')

print(window_root.style.theme_names())
#style = ttk.Style()
#style.theme_use('alt')





#style.configure("BW.TLabel",foreground="black",background="white")

#label = ttk.Label(window_root, text="label1", style="BW.TLabel" )
#label.pack()
#button = ttk.Button(text='Push to get your chash')
#button.grid(row=3 , column=2)
#label.pack()
#style = tk.Style()
#style.configure("BW.TLabel",foreground="black",background="white")

window_root.mainloop()