"""The Main UI"""
import tkinter as tk
from tkinter import ttk

from graphs import GraphFactory, Storytelling
from descstat import DescStat
from path_ui import PathUI
import matplotlib.pyplot as plt


class TabManager(tk.Tk):
    """The Main UI of the program"""
    def __init__(self) -> None:
        super().__init__()
        self.title('UK Flight')
        self.protocol('WM_DELETE_WINDOW', exit)
        self.graph_factory = GraphFactory
        self.graph_dict = {'Compare Delay with Previous Year':'Corr',
                           'Flights Cancelled vs Overall Flights' : 'Pie',
                           'Distribution of Delays' : 'Dist',
                           'Comparing Flight Cancellations' : 'flights_cancelled_percent',
                           'Comparing Average Delays' : 'average_delay_mins'}
        self.init_components()

    def init_components(self):
        """Initialise components"""
        pack = {'side':'left', 'expand':True, 'fill':'both'}
        self.create_menu_bar()
        self.tab_controller = ttk.Notebook(self)

        self.path_ui = PathUI(self)
        self.path_ui.pack(pack)
        self.tab_controller.add(self.path_ui, text='Find Flight Path')

        self.storytelling = Storytelling(self)
        self.storytelling.pack(pack)
        self.tab_controller.add(self.storytelling, text='Data Storytelling')

        self.desc_stat = DescStat(self)
        self.desc_stat.pack(pack)
        self.tab_controller.add(self.desc_stat, text='Descriptive Statistics')

        for key,val in self.graph_dict.items():
            graph = self.graph_factory.get_instance(val, self)
            graph.pack(pack)
            self.tab_controller.add(graph, text=key)
        self.tab_controller.pack(pack)

    def create_menu_bar(self):
        """Creates the menu bar on the top of the screen"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        menubar.add_command(label='Exit', command=self.exit)

    def get_all_graphs(self):
        """Get all graphs, use in feed_data"""
        return self.graph_factory.instances.values()

    def get_current_tab_name(self) -> str:
        """Get the name of the tab that's currently active"""
        try:
            return self.graph_dict[self.tab_controller.tab(self.tab_controller.select(), "text")]
        except KeyError:
            return self.tab_controller.tab(self.tab_controller.select(), "text")

    def get_current_graph(self) -> tk.Frame:
        """Get the graph that's currently displayed"""
        current_tab = self.get_current_tab_name()
        current_graph = self.graph_factory.get_instance(current_tab)
        return current_graph

    def exit(self) -> None:
        """Closes all graphs"""
        plt.close('all')
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()

    def run(self) -> None:
        """Runs the mainloop"""
        self.mainloop()

    def bind_tab_selected(self, func, add=None):
        """Binds action when a tab is selected"""
        def bind_function(event):
            func(self.get_current_tab_name())
        self.tab_controller.bind("<<NotebookTabChanged>>", bind_function, add)

if __name__ == '__main__':
    root = tk.Tk()
    a = GraphFactory.get_instance('Corr', root)
    b = GraphFactory.get_instance('Corr', root)
    print(id(a))
    print(id(b))
