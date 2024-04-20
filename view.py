import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd


class UI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('UK Flight')
        self.init_components()

    def init_components(self):
        tab_controller = ttk.Notebook(self)

        actual_tab = ControlPanel(self)
        actual_tab.pack(padx=20, pady=20, anchor='e',expand=True, fill='both')
        tab_controller.add(actual_tab, text='test_tab')
        tab_controller.pack(expand=True, fill='both')

    def run(self):
        self.mainloop()


class ControlPanel(tk.Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.selector_instances = {}
        self.init_components()

    def init_components(self):
        if 'origin' not in self.selector_instances:
            self.create_selector('origin')
        data = pd.DataFrame({
                            'Python': [11.27,69],
                            'C': [2,3],
                            'Java': [10.46,2],
                            'C++': [7.5,1],
                            'C#': [5.26,3]
                            })
        fig, ax = plt.subplots(figsize=(3,3))
        canvas = FigureCanvasTkAgg(fig, self)
        sns.barplot(data=data)
        canvas.get_tk_widget().pack(side='left', expand=True)

        for val in self.selector_instances.values():
            val.pack(side='right')

    def create_selector(self, label):
        selector = Selector()
        selector.set_label(label)
        self.selector_instances[label] = selector


class Selector(tk.Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.pack_options = {'anchor':tk.CENTER}
        self.label_textvar = tk.StringVar()
        self.init_components()

    def init_components(self):
        label = tk.Label(self, textvariable=self.label_textvar)
        self.selector = ttk.Combobox(self)
        label.pack(self.pack_options)
        self.selector.pack(self.pack_options)

    def set_label(self, text:str) -> None:
        self.label_textvar.set(text)

    def set_selector_val(self, val:list) -> None:
        self.selector['values'] = val

if __name__ == '__main__':
    UI().run()
