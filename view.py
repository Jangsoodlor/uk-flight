import tkinter as tk
from tkinter import ttk
import abc

import random

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns
import pandas as pd


class TabManager(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('UK Flight')
        self.graphs = {}
        self.init_components()

    def init_components(self):
        tab_controller = ttk.Notebook(self)
        pack = {'side':'left', 'expand':True, 'fill':'both'}
        graph_dict = {'Compare Delay with Previous Year': CorrGraph}
        for key, val in graph_dict.items():
            graph = val(self)
            self.graphs[key] = graph
            graph.pack(pack)
            tab_controller.add(graph, text=key)
        tab_controller.pack(expand=True, fill='both')

    def exit(self):
        plt.close('all')

    def run(self):
        self.protocol('WM_DELETE_WINDOW', exit)
        self.mainloop()

class Graph(tk.Frame, abc.ABC):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.init_components()

    def init_components(self):
        self.side_panel = SidePanel(self)
        self.side_panel.pack(side='right', padx=10)
        self.add_side_panel_elements()

        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=self)
        NavigationToolbar2Tk(self.canvas, self)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

    @abc.abstractmethod
    def add_side_panel_elements(self):
        raise NotImplementedError('Abstract Method')

    @abc.abstractmethod
    def plot_graph(self, caller):
        raise NotImplementedError('Abstract Method')

    @property
    @abc.abstractmethod
    def get_first_combobox(self):
        raise NotImplementedError('Abstract Property')

class CorrGraph(Graph):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)

    def add_side_panel_elements(self):
        self.side_panel.create_selector('Airport')
        self.side_panel.create_selector('Origin (Optional)')
        self.side_panel.create_selector('Destination (Optional)')
        self.side_panel.create_button('PLOT')
        self.side_panel.bind_button('PLOT', self.plot_graph)

    def plot_graph(self, caller):
        a = lambda : random.randint(1,100)
        data = pd.DataFrame({
                            'Python': [a(), a()],
                            'C': [a(), a()],
                            'Java': [a(), a()],
                            'C++': [a(), a()],
                            'C#': [a(), a()]
                            })
        sns.barplot(data=data)
        self.canvas.draw()

    @property
    def get_first_combobox(self):
        return 'Airport'

class SidePanel(tk.Frame):
    def __init__(self, master=None,cnf={},**kwargs):
        super().__init__(master, cnf, **kwargs)
        self.selectors = {}
        self.buttons = {}
        self.padding = {'pady':10}

    def create_selector(self, name):
        selector = Selector(self)
        selector.label = name
        self.selectors[name] = selector
        selector.set_state('disabled')
        selector.pack(self.padding)

    def get_selector(self, name):
        if name in self.selectors:
            return self.selectors[name]
        return None

    def set_selector_value(self, name, val):
        self.selectors[name].combobox_val = val

    def hide_selector(self, name):
        self.get_selector(name).pack_forget()

    def unhide_selector(self, name):
        temp_list = list(self.selectors)
        temp_list = temp_list[temp_list.index(name)+1:]
        for id in temp_list:
            self.hide_selector(id)
        self.get_selector(name).pack(self.padding)
        for id in temp_list:
            self.get_selector(id).pack(self.padding)

    def create_button(self, name):
        button = tk.Button(self, text=name)
        self.buttons[name] = button
        button.pack(self.padding)

    def bind_button(self, name, command):
        self.buttons[name].bind('<Button>', command)

class Selector(tk.Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.__label_var = tk.StringVar()
        self.__combobox_var = tk.StringVar()
        self.init_components()

    def init_components(self):
        label = tk.Label(self, textvariable=self.__label_var)
        self.__combobox = ttk.Combobox(self, textvariable=self.__combobox_var)
        pack = {'anchor':tk.CENTER}
        label.pack(pack)
        self.__combobox.pack(pack)

    @property
    def label(self) -> None:
        return self.__label_var.get()

    @label.setter
    def label(self, text:str) -> None:
        self.__label_var.set(text)

    @property
    def combobox_val(self):
        return self.__combobox_var.get()

    @combobox_val.setter
    def combobox_val(self, val:list) -> None:
        self.__combobox['values'] = val

    def set_state(self, state):
        self.__combobox['state'] = state

if __name__ == '__main__':
    a = TabManager()
    a.run()
