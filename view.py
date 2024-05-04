"""The Main UI"""
import tkinter as tk
from tkinter import ttk

from graphs import GraphFactory
import matplotlib.pyplot as plt


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

if __name__ == '__main__':
    root = tk.Tk()
    a = GraphFactory.get_instance('Corr', root)
    b = GraphFactory.get_instance('Corr', root)
    print(id(a))
    print(id(b))
