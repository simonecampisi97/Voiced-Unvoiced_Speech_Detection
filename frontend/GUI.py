import tkinter as tk

window_root = tk.Tk()

window_root.geometry("800x600")
window_root.title('Voiced/Unvoiced-speech detection')
window_root.resizable(False, False)

label = tk.Label(window_root, text="label1")

button = tk.Button(text='Push to get your chash')
button.place(x=300, y=0)
# label.pack()


window_root.mainloop()
