import tkinter as tk
from tkinter import ttk

def set_appearance_mode(mode):
    pass

class CTk(tk.Tk):
    pass

class CTkFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)

class CTkLabel(tk.Label):
    def __init__(self, master=None, text="", **kwargs):
        super().__init__(master, text=text)
    def pack(self, **kwargs):
        super().pack(**kwargs)

class CTkEntry(tk.Entry):
    def __init__(self, master=None, width=None, placeholder_text=None, **kwargs):
        super().__init__(master, **kwargs)
    def pack(self, **kwargs):
        super().pack(**kwargs)
    def get(self):
        return super().get()
    def insert(self, index, value):
        return super().insert(index, value)
    def delete(self, first, last=None):
        return super().delete(first, last)

class CTkButton(tk.Button):
    def __init__(self, master=None, text="", command=None, width=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
    def pack(self, **kwargs):
        super().pack(**kwargs)

class CTkOptionMenu(tk.Frame):
    def __init__(self, master=None, values=None, **kwargs):
        super().__init__(master)
        self._var = tk.StringVar(master)
        vals = values or []
        # use first value if exists
        default = vals[0] if vals else ""
        self._var.set(default)
        self._om = ttk.OptionMenu(self, self._var, default, *vals)
        self._om.pack(fill='x')
    def pack(self, **kwargs):
        super().pack(**kwargs)
    def get(self):
        return self._var.get()
    def set(self, value):
        self._var.set(value)

# expose simple constants
CTk.set_appearance_mode = staticmethod(set_appearance_mode)

# Backwards compatibility names
set_appearance_mode = set_appearance_mode
