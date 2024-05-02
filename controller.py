from view import TabManager
from model import Model

class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.feed_init_data()

    def run(self):
        self.view.run()

    def feed_init_data(self):
        """filled the first selector of each graph with initial datas.
        And bind the plot button."""
        graphs = self.view.get_all_graphs()
        for graph in graphs:
            first_box_name = graph.side_panel.first_selector
            data = self.model.get_selector_data(first_box_name.label)
            first_box_name.val = data
            graph.side_panel.disable_next_selectors(first_box_name.label)
            graph.side_panel.bind_selectors(self.selector_selected)
            self.bind_plot_buttons(graph)
            

    def bind_plot_buttons(self, graph):
        graph.side_panel.bind_button('PLOT', self.activate_plot)

    def activate_plot(self, event):
        graph = self.view.get_current_graph()
        graph_name = self.view.get_current_tab_name()
        options = graph.side_panel.get_selector_options()
        data = self.model.get_graph_data(graph_name, options)
        graph.plot_graph(data[0], data[1])
        

    def selector_selected(self, selector_name):
        """Fill the next selector with data after the first one is selected"""
        current_graph = self.view.get_current_graph()
        next_selector = current_graph.side_panel.get_next_selector(selector_name)
        if next_selector:
            current_graph.side_panel.disable_next_selectors(selector_name)
            filters = current_graph.side_panel.get_selector_options()
            data = self.model.get_selector_data(next_selector.label, filters)
            next_selector.val = data
