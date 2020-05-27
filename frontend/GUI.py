import tkinter as tk
from frontend.Widget.Window import Window



button = tk.Button(text='Push to get your chash')
button.place(x=300, y=5)
# label.pack()
window_root = Window(title='VOICED/UNVOICED DETECTION', geometry='600x800',resizable=(False,False))
window_root.mainloop()
