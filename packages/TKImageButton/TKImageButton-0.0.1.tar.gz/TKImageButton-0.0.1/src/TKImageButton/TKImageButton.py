import tkinter as tk

class ImageButton(tk.Button):
    def __init__(self, master, source, command, **kwargs):
        super().__init__(master, **kwargs)
        self.image = tk.PhotoImage(file=source)
        self.config(image=self.image, borderwidth=0, highlightthickness=0, bd=0, bg="White", activebackground="White")
        self.config(command=command)
