"""A UI for Descriptive Statistic Tab"""
import tkinter as tk
from tkinter import ttk

class DescStat(tk.Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.__combobox_var = tk.StringVar()
        self.init_components()

    def init_components(self):
        top_frame = tk.Frame(self)
        label = tk.Label(top_frame, text='Select Airport')
        self.__combobox = ttk.Combobox(top_frame, textvariable=self.__combobox_var)
        self.__combobox['state'] = 'readonly'
        label.pack(side='left')
        self.__combobox.pack(side='right')
        top_frame.pack(side='top', anchor=tk.W, padx=10, pady=10)

        self.__textbox = tk.Text(self)
        self.__textbox['state'] = 'disabled'
        self.__textbox.pack(expand=True, fill='both')

    def binder(self, func, add=None):
        """Binds the combobox"""
        def bind_function(event):
            func(self.__combobox_var.get())
        self.__combobox.bind('<<ComboboxSelected>>', bind_function, add)

    def insert_text(self, text):
        self.__textbox['state'] = 'normal'
        self.__textbox.delete(1.0, tk.END)
        self.__textbox.insert(tk.END, text)
        self.__textbox['state'] = 'disabled'

    @property
    def val(self):
        """Get the value of the combobox"""
        return self.__combobox_var.get()

    @val.setter
    def val(self, val:list) -> None:
        """Set combobox value"""
        self.__combobox['values'] = val
        self.__combobox_var.set('')

if __name__ == '__main__':
    root = tk.Tk()
    frame = DescStat(root)
    frame.pack(expand=True, fill='both')
    frame.insert_text('hello')
    root.mainloop()