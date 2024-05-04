"""The Main UI and UI components of uk-flight application"""
import tkinter as tk
from tkinter import ttk
import abc

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns


class TabManager(tk.Tk):
    """The Main UI of the program"""
    def __init__(self) -> None:
        super().__init__()
        self.title('UK Flight')
        self.graph_factory = GraphFactory
        self.graph_dict = {'Compare Delay with Previous Year':'Corr',
                           'Flights Cancelled vs Overall Flights' : 'Pie',
                           'Distribution of Delays' : 'Dist',
                           'Comparing Flight Cancellations' : 'flights_cancelled_percent',
                           'Comparing Average Delays' : 'average_delay_mins'}
        self.init_components()

    def init_components(self):
        """Initialise components"""
        self.create_menu_bar()
        self.tab_controller = ttk.Notebook(self)
        pack = {'side':'left', 'expand':True, 'fill':'both'}
        for key,val in self.graph_dict.items():
            graph = self.graph_factory.get_instance(val, self)
            graph.pack(pack)
            self.tab_controller.add(graph, text=key)
        self.tab_controller.pack(expand=True, fill='both')

    def create_menu_bar(self):
        """Creates the menu bar on the top of the screen"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        help_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Help", menu=help_menu)
        menubar.add_command(label='Exit', command=self.kill)

    def kill(self):
        """Kills the process"""
        self.exit()
        self.destroy()

    def get_all_graphs(self):
        """Get all graphs, use in feed_data"""
        return self.graph_factory.instances.values()

    def get_current_tab_name(self) -> str:
        """Get the name of the tab that's currently active"""
        return self.graph_dict[self.tab_controller.tab(self.tab_controller.select(), "text")]

    def get_current_graph(self) -> tk.Frame:
        """Get the graph that's currently displayed"""
        current_tab = self.get_current_tab_name()
        current_graph = self.graph_factory.get_instance(current_tab)
        return current_graph

    def exit(self) -> None:
        """Closes all graphs"""
        plt.close('all')

    def run(self) -> None:
        """Runs the mainloop"""
        self.protocol('WM_DELETE_WINDOW', exit)
        self.mainloop()

class GraphFactory(tk.Frame, abc.ABC):
    """A Factory of various types of Tabs that has a Graph
    with an attached side panel"""

    instances = {}

    @classmethod
    def get_instance(cls, name, master=None):
        """Gets graph instance"""
        if name not in cls.instances:
            factories = {'Corr': CorrGraph,
                         'Pie' : PieGraph,
                         'Dist' : DistributionGraph,
                         'average_delay_mins' : BarGraph,
                         'flights_cancelled_percent' : BarGraph}
            if name not in factories:
                raise ValueError('Invalid graph')
            if master is None:
                raise ValueError('Master Needed to initialise graph')
            cls.instances[name] = factories[name](master)
        return cls.instances[name]

    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.__description = tk.StringVar()
        self.init_components()

    @property
    def description(self) -> str:
        """Get the description of the tab"""
        return self.__description.get()

    @description.setter
    def description(self, text:str):
        """Set the description of the tab"""
        self.__description.set(text)

    def init_components(self):
        """Initialise components"""
        self.side_panel = SidePanel(self)
        self.side_panel.pack(side='right', padx=10)
        self.add_side_panel_elements()

        graph_frame = tk.Frame(self)
        label = tk.Label(graph_frame, textvariable=self.__description)
        label.pack(anchor=tk.W, side=tk.BOTTOM)

        self.fig, self.ax = plt.subplots(dpi=90)
        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=graph_frame)
        NavigationToolbar2Tk(self.canvas, graph_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')
        graph_frame.pack(expand=True, fill='both')

    @abc.abstractmethod
    def add_side_panel_elements(self):
        """An abstract method to add elements to the side panel"""
        raise NotImplementedError('Abstract Method')

    @abc.abstractmethod
    def plot_graph(self, data, title):
        """An abstract method to plot the graphs"""
        raise NotImplementedError('Abstract Method')


class CorrGraph(GraphFactory):
    """A Correlation Graph tab"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)

    def add_side_panel_elements(self):
        """Add side panel elements for correlation graph"""
        self.description = 'See correlation of average delay of airlines'
        self.side_panel.create_selector('Airline')
        self.side_panel.create_selector('Origin (Optional)')
        self.side_panel.create_selector('Destination (Optional)')
        self.side_panel.create_button('PLOT')

    def plot_graph(self, data, title):
        """Plots the correlation graph and set correlation coefficient"""
        self.ax.clear()
        sns.scatterplot(x="average_delay_mins",
                        y="previous_year_month_average_delay",
                        data=data, ax=self.ax)
        self.description = title[0]
        self.ax.set_xlabel("Average Delay in January 2024 (minutes)")
        self.ax.set_ylabel("Average Delay in January 2023 (minutes)")
        self.ax.set_title(title[1])
        self.canvas.draw()


class PieGraph(GraphFactory):
    """A Pie Graph Tab"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)

    def add_side_panel_elements(self):
        """Add side panel elements for the pie graph"""
        self.description = 'See the amount of flights cancelled compared to all flights'
        self.side_panel.create_selector('Origin')
        self.side_panel.create_selector('Destination')
        self.side_panel.create_selector('Airline')
        self.side_panel.create_button('PLOT')

    def plot_graph(self, data,title):
        """Plots the pie graph"""
        self.ax.clear()
        self.ax.pie(data, startangle=90, counterclock=False, autopct='%1.1f%%', pctdistance=1.15,
                    labeldistance=1.25, radius = 0.9)
        self.ax.set_title(title)
        self.ax.legend(['Flights not Cancelled', 'Flights Cancelled'])
        self.ax.set_title(title)
        self.canvas.draw()


class DistributionGraph(GraphFactory):
    """A distribution graph tab"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)

    def add_side_panel_elements(self):
        """Add side panel elements to the distribution graph"""
        self.description = 'See the distribution of delays'
        self.side_panel.create_selector('Origin')
        self.side_panel.create_selector('Destination')
        self.side_panel.create_selector('Airline')
        self.side_panel.create_button('PLOT')

    def plot_graph(self, data, title):
        """Plots the distribution graph"""
        self.ax.clear()
        sns.barplot(x=data['Interval'], y=data['Percent'], ax=self.ax)
        interval_label = [
            '< -15',
            '[-15,1]',
            '[0,15]',
            '[16,30]',
            '[31,60]',
            '[61,120]',
            '[121,180]',
            '[181,360]',
            '> 360',
        ]
        self.ax.set_xticks([i for i in range(9)])
        self.ax.set_xticklabels(interval_label)
        self.ax.set_xlabel('Delay Interval (minutes)')
        self.ax.set_title(title)
        self.canvas.draw()

class BarGraph(GraphFactory):
    """A BarGraph tab"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)

    def add_side_panel_elements(self):
        self.side_panel.add_history_box()
        self.side_panel.create_selector('Origin (Optional)')
        self.side_panel.create_selector('Destination (Optional)')
        self.side_panel.create_selector('Airline')
        self.side_panel.create_button('ADD')
        self.side_panel.create_button('REMOVE')
        self.side_panel.create_button('PLOT')
        self.side_panel.set_button_state('REMOVE', 'disabled')
        self.side_panel.set_button_state('ADD', 'disabled')

    def plot_graph(self, data, title):
        self.ax.clear()
        sns.barplot(x=data[0], y=data[1], ax=self.ax)
        self.ax.set_title(title)
        self.canvas.draw()


class SidePanel(tk.Frame):
    """The side panel frame"""
    def __init__(self, master=None,cnf={},**kwargs):
        super().__init__(master, cnf, **kwargs)
        self.__selectors = {}
        self.__buttons = {}
        self.__padding = {'pady':10}
        self.history_box = None

    def create_selector(self, name):
        """Creates a selector object"""
        selector = Selector(self)
        selector.label = name
        self.__selectors[name] = selector
        selector.set_state('readonly')
        selector.pack(self.__padding)

    def add_history_box(self):
        """add historybox object to the side panel"""
        self.history_box = HistoryBox(self)
        self.history_box.pack(self.__padding)

    @property
    def is_history_box(self) -> bool:
        """Returns True if there's a historybox instance inside, returns false otherwise"""
        return bool(self.history_box)

    def get_selector(self, name):
        """Get selector by name"""
        if name in self.__selectors:
            return self.__selectors[name]
        return None

    @property
    def first_selector(self):
        """returns the first selector in the side panel"""
        name = iter(self.__selectors)
        c = next(name)
        return self.__selectors[c]

    def get_next_selector(self, name=None):
        """Returns the selector that is located immediately below the one specified
        Return None if there isn't any"""
        temp_list = list(self.__selectors)
        if not name:
            return self.__selectors[temp_list[0]]
        index = temp_list.index(name)+1
        if index < len(temp_list):
            return self.__selectors[temp_list[index]]
        return None

    def disable_next_selectors(self, name):
        """Disable all selector objects located below the current one"""
        temp_list = list(self.__selectors)
        temp_list = temp_list[temp_list.index(name)+1:]
        for i in temp_list:
            self.get_selector(i).set_state('disabled')

    def get_selector_options(self):
        """Returns the options filled in the selector"""
        temp_dict = {}
        for selector in self.__selectors.values():
            temp_dict[selector.label] = selector.val
        return temp_dict

    def bind_selectors(self, func, add=None):
        """Bind all selectors to a specific function"""
        for selector in self.__selectors.values():
            selector.bind(func, add)

    def bind_selector(self, name, func, add=None):
        """Bind a specific selector"""
        self.__selectors[name].bind(func, add)

    def create_button(self, name):
        """Creates a button"""
        button = tk.Button(self, text=name)
        self.__buttons[name] = button
        button.pack(self.__padding)

    def bind_button(self, name, func, add=None):
        """bind a button to a specific function"""
        self.__buttons[name].bind('<Button>', func)

    def get_button_state(self, name):
        """Get a state of a button"""
        return self.__buttons[name]['state']

    def set_button_state(self, name, state):
        """Set a state of a button"""
        self.__buttons[name]['state'] = state

    def hide_selector(self, name):
        """Hide a selector"""
        self.get_selector(name).pack_forget()

    def unhide_selector(self, name):
        """Unhide a selector"""
        temp_list = list(self.__selectors)
        temp_list = temp_list[temp_list.index(name)+1:]
        for i in temp_list:
            self.hide_selector(i)
        self.get_selector(name).pack(self.__padding)
        for i in temp_list:
            self.get_selector(i).pack(self.__padding)


class HistoryBox(tk.Frame):
    """A frame that consists of a scroll bar and a listbox. It keeps track of
    what the user has selected from the selector"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.init_components()

    def init_components(self):
        """Initialise components"""
        self.__listbox = tk.Listbox(self)
        label = tk.Label(self, text='Selected Airlines')
        label.pack()
        scrollbar = tk.Scrollbar(self,
                                      orient='vertical',
                                      command=self.__listbox.yview)
        self.__listbox.config(yscrollcommand=scrollbar.set)
        self.__listbox.pack(side='left')
        self.__listbox_val = []
        scrollbar.pack(side='right', expand=True, fill='y')

    def __update(self):
        """Update the historybox"""
        self.__listbox['listvariable'] = tk.Variable(value=self.__listbox_val)

    @property
    def values(self):
        """Get the listbox"""
        return self.__listbox_val

    @values.setter
    def values(self, lst):
        """Set the listbox values"""
        self.__listbox_val = lst
        if not lst:
            self.__listbox.selection_clear(0, 'end')
        self.__update()

    def append(self, val):
        """Add new element to the end of the listbox"""
        self.__listbox_val.append(val)
        self.__update()

    def remove(self, val):
        """Removes an element from the listbox"""
        self.__listbox_val.remove(val)
        self.__update()

    def bind(self, func, add=None):
        """Bind the listbox. It'll inject the function with the current selection"""
        try:
            def bind_function(event):
                cur_sel = self.__listbox.get(self.__listbox.curselection())
                func(cur_sel)
            self.__listbox.bind('<<ListboxSelect>>', bind_function, add)
        except Exception:
            pass

class Selector(tk.Frame):
    """An object that consists of a label and a combobox"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.__label_var = tk.StringVar()
        self.__combobox_var = tk.StringVar()
        self.init_components()

    def init_components(self):
        """init components"""
        label = tk.Label(self, textvariable=self.__label_var)
        self.__combobox = ttk.Combobox(self, textvariable=self.__combobox_var)
        pack = {'anchor':tk.CENTER}
        label.pack(pack)
        self.__combobox.pack(pack)

    def set_state(self, state):
        """Set the state of the combobox"""
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
        """Return label"""
        return self.__label_var.get()

    @label.setter
    def label(self, text:str) -> None:
        """Set the label"""
        self.__label_var.set(text)

    @property
    def val(self):
        """Get the value of the combobox"""
        return self.__combobox_var.get()

    @val.setter
    def val(self, val:list) -> None:
        """Set combobox value"""
        self.__combobox['values'] = val
        self.__combobox['state'] = 'readonly'
        self.__combobox_var.set('')

    def set_selected(self, val:str):
        """Set the combobox value"""
        self.__combobox_var.set(val)

if __name__ == '__main__':
    root = tk.Tk()
    a = GraphFactory.get_instance('Corr', root)
    b = GraphFactory.get_instance('Corr', root)
    print(id(a))
    print(id(b))
