"""Class for Graphs"""
import tkinter as tk
import abc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns
from side_panel import SidePanel

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

    # @abc.abstractmethod
    # def make_random_options(self):
    #     raise NotImplementedError('Abstract Method')


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
        self.ax.set_xlabel("Average Delay in January 2024 (minutes)")
        self.ax.set_ylabel("Average Delay in January 2023 (minutes)")
        self.ax.set_title(title)
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
        self.description = 'Compare flaws of various airlines'
        self.side_panel.add_history_box()
        self.side_panel.create_selector('Origin (Optional)')
        self.side_panel.create_selector('Destination (Optional)')
        self.side_panel.create_selector('Airline')
        self.side_panel.create_button('ADD')
        self.side_panel.create_button('REMOVE')
        self.side_panel.create_button('PLOT')
        self.side_panel.hide_button('PLOT')
        self.side_panel.set_button_state('REMOVE', 'disabled')
        self.side_panel.set_button_state('ADD', 'disabled')

    def plot_graph(self, data, title):
        self.ax.clear()
        sns.barplot(x=data[0], y=data[1], ax=self.ax)
        self.ax.set_title(title)
        self.ax.set_xlabel('Airlines')
        if 'average_delay_mins' in title:
            self.ax.set_ylabel('Average Delay (minutes)')
        else:
            self.ax.set_ylabel('Percentage')
        self.canvas.draw()

class Storytelling(tk.Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.plotted = False
        self.init_components()

    def init_components(self):
        self.fig, self.ax = plt.subplots(2,3,layout='constrained')
        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=self)
        self.canvas.get_tk_widget().pack(side='left', fill='both', expand=True)
        self.label_frame = tk.Frame(self)
        self.label_frame.pack(side='right', fill='both', expand=True)

    def plot_graph(self, datas):
        if not self.plotted:
            methods = [self.__plot_pie,
                    self.__plot_corr,
                    self.__plot_box,
                    self.__plot_hist,
                    self.__plot_bar,
                    self.__plot_bar]

            for ax, data, method in zip(self.ax.ravel(), datas[0], methods):
                graph_data = data[0]
                title = data[1]
                method(ax, graph_data, title)
            self.canvas.draw()
            self.__create_desc_stat_labels(datas[1])
            self.plotted = True

    def __create_desc_stat_labels(self, data):
        for i in data.split('\n'):
            label = tk.Label(self.label_frame, text=i)
            label.pack(anchor='w', padx=10, pady=5)


    def __plot_pie(self, ax, data, title):
        ax.pie(data, startangle=90, counterclock=False, autopct='%1.1f%%', pctdistance=1.15,
                    labeldistance=1.25, radius = 0.9)
        ax.set_title(title)
        ax.legend(['Flights not Cancelled', 'Flights Cancelled'])
        ax.set_title(title)

    def __plot_corr(self, ax, data, title):
        sns.scatterplot(x="average_delay_mins",
                        y="previous_year_month_average_delay",
                        data=data, ax=ax)
        ax.set_xlabel("Delays in January 2024 (minutes)")
        ax.set_ylabel("Delays in January 2023 (minutes)")
        ax.set_title(title)

    def __plot_box(self, ax, data, title):
        sns.boxplot(data=data, ax=ax)
        ax.set_title(title)

    def __plot_hist(self, ax, data, title):
        sns.barplot(x=data['Interval'], y=data['Percent'], ax=ax)
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
        ax.set_xticks([i for i in range(9)])
        ax.set_xticklabels(interval_label)
        ax.set_xlabel('Delay Interval (minutes)')
        ax.set_title(title)
        ax.tick_params(axis='x', labelrotation=45)

    def __plot_bar(self, ax, data, title):
        bar = sns.barplot(x=data[0], y=data[1], ax=ax)
        for item in bar.get_xticklabels():
            item.set_rotation(20)
        if 'Delays' in title:
            ax.set_ylabel('Average Delay (minutes)')
        else:
            ax.set_ylabel('Percentage')
        ax.set_title(title)
