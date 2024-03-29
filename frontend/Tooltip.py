from frontend.Settings import *
import tkinter as tk
import tkinter.ttk as ttk


class ToolTip:

    def __init__(self, widget, text, timeout=DEFAULT_TOOLTIP_TIME):
        """
        :param widget: The tkinter widget
        :type widget: widget type varies
        :param text: text for the tooltip. It can inslude \n
        :type text: str
        :param timeout: Time in milliseconds that mouse must remain still before tip is shown
        :type timeout: int
        """
        self.widget = widget
        self.text = text
        self.timeout = timeout
        # self.wraplength = wraplength if wraplength else widget.winfo_screenwidth() // 2
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        """
        Called by tkinter when mouse enters a widget
        :param event:  from tkinter.  Has x,y coordinates of mouse

        """
        self.x = event.x
        self.y = event.y
        self.schedule()

    def leave(self, event=None):
        """
        Called by tktiner when mouse exits a widget
        :param event:  from tkinter.  Event info that's not used by function.

        """
        self.unschedule()
        self.hidetip()

    def schedule(self):
        """
        Schedule a timer to time how long mouse is hovering
        """
        self.unschedule()
        self.id = self.widget.after(self.timeout, self.showtip)

    def unschedule(self):
        """
        Cancel timer used to time mouse hover
        """
        if self.id:
            self.widget.after_cancel(self.id)
        self.id = None

    def showtip(self):
        """
        Creates a topoltip window with the tooltip text inside of it
        """
        if self.tip_window:
            return
        x = self.widget.winfo_rootx() + self.x + DEFAULT_TOOLTIP_OFFSET[0]
        y = self.widget.winfo_rooty() + self.y + DEFAULT_TOOLTIP_OFFSET[1]
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry("+%d+%d" % (x, y))
        self.tip_window.wm_attributes("-topmost", 1)

        label = ttk.Label(self.tip_window, text=self.text, justify=tk.LEFT,
                          background=TOOLTIP_BACKGROUND_COLOR, relief=tk.SOLID, borderwidth=1)
        if TOOLTIP_FONT is not None:
            label.config(font=TOOLTIP_FONT)
        label.pack()

    def hidetip(self):
        """
        Destroy the tooltip window
        """
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None
