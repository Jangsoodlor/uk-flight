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
        self.graph_factory = GraphFactory
        self.graph_dict = {'Compare Delay with Previous Year':'Corr'}
        self.init_components()

    def init_components(self):
        self.tab_controller = ttk.Notebook(self)
        pack = {'side':'left', 'expand':True, 'fill':'both'}
        for key,val in self.graph_dict.items():
            graph = self.graph_factory.get_instance(val, self)
            graph.pack(pack)
            self.tab_controller.add(graph, text=key)
        self.tab_controller.pack(expand=True, fill='both')

    def exit(self):
        plt.close('all')

    def run(self):
        self.protocol('WM_DELETE_WINDOW', exit)
        self.mainloop()

    def get_all_graphs(self):
        return self.graph_factory.instances.values()

    def get_current_tab(self):
        return self.tab_controller.tab(self.tab_controller.select(), "text")

class GraphFactory(tk.Frame, abc.ABC):

    instances = {}

    @classmethod
    def get_instance(cls, name, master=None):
        """Gets graph instance"""
        if name not in cls.instances:
            factories = {'Corr': CorrGraph}
            if name not in factories:
                raise ValueError('Invalid graph')
            if master is None:
                raise ValueError('Master Needed to initialise graph')
            cls.instances[name] = factories[name](master)
        return cls.instances[name]

    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.__description = tk.StringVar()
        self.__description.set('hello')
        self.init_components()

    def init_components(self):
        self.side_panel = SidePanel(self)
        self.side_panel.pack(side='right', padx=10)
        self.add_side_panel_elements()

        graph_frame = tk.Frame(self)
        label = tk.Label(graph_frame, textvariable=self.__description)
        label.pack(anchor=tk.W)

        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=graph_frame)
        NavigationToolbar2Tk(self.canvas, graph_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')
        graph_frame.pack(expand=True, fill='both')

    @abc.abstractmethod
    def add_side_panel_elements(self):
        raise NotImplementedError('Abstract Method')

    @abc.abstractmethod
    def plot_graph(self, caller):
        raise NotImplementedError('Abstract Method')


class CorrGraph(GraphFactory):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)

    def add_side_panel_elements(self):
        self.side_panel.create_selector('Airline')
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
        selector.set_state('readonly')
        selector.pack(self.padding)

    def get_selector(self, name):
        """Get selector by name"""
        if name in self.selectors:
            return self.selectors[name]
        return None

    @property
    def first_selector(self):
        name = iter(self.selectors)
        c = next(name)
        return self.selectors[c]

    def get_next_selector(self, name=None):
        """Returns the selector that is located immediately below the one specified
        Return None if there isn't any"""
        temp_list = list(self.selectors)
        if not name:
            return self.selectors[temp_list[0]]
        index = temp_list.index(name)+1
        if index < len(temp_list):
            return self.selectors[temp_list[index]]
        return None

    def disable_next_selectors(self, name):
        """Disable all selector objects located below the current one"""
        temp_list = list(self.selectors)
        temp_list = temp_list[temp_list.index(name)+1:]
        for i in temp_list:
            self.get_selector(i).set_state('disabled')

    def get_selector_options(self):
        temp_dict = {}
        for selector in self.selectors.values():
            temp_dict[selector.label] = selector.val
        return temp_dict

    def create_button(self, name):
        button = tk.Button(self, text=name)
        self.buttons[name] = button
        button.pack(self.padding)

    def bind_button(self, name, command):
        self.buttons[name].bind('<Button>', command)

    def bind_selectors(self, func, add=None):
        for selector in self.selectors.values():
            selector.bind(func, add)

    def hide_selector(self, name):
        self.get_selector(name).pack_forget()

    def unhide_selector(self, name):
        temp_list = list(self.selectors)
        temp_list = temp_list[temp_list.index(name)+1:]
        for i in temp_list:
            self.hide_selector(i)
        self.get_selector(name).pack(self.padding)
        for i in temp_list:
            self.get_selector(i).pack(self.padding)

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

    def set_state(self, state):
        self.__combobox['state'] = state
        if state == 'disabled':
            self.__combobox_var.set('')
            self.__combobox['values'] = []

    def bind(self, func, add=None):
        """Binds the combobox"""
        def bind_function(event):
            func(self.__label_var.get())
        self.__combobox.bind('<<ComboboxSelected>>', bind_function, add)

    @property
    def label(self) -> None:
        return self.__label_var.get()

    @label.setter
    def label(self, text:str) -> None:
        self.__label_var.set(text)

    @property
    def val(self):
        return self.__combobox_var.get()

    @val.setter
    def val(self, val:list) -> None:
        self.__combobox['values'] = val
        self.__combobox['state'] = 'readonly'
        self.__combobox_var.set('')

if __name__ == '__main__':
    root = tk.Tk()
    a = GraphFactory.get_instance('Corr', root)
    b = GraphFactory.get_instance('Corr', root)
    print(id(a))
    print(id(b))
