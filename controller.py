"""The controller. Which controls interaction between view and model"""
from tkinter import messagebox

class Controller:
    """The Controller class"""
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.feed_init_data()

    def run(self):
        """Run the app"""
        self.view.run()

    def feed_data(self, graph, name, filters=None):
        """Set the data of a certain combobox in a specific graph"""
        panel = graph.side_panel
        selector =  panel.get_selector(name)
        data = self.model.get_selector_data(selector.label, filters)
        data.sort()
        selector.val = [''] + data

    def feed_init_data(self):
        """Fill the first selectors of each tab with initial data"""
        self.feed_graphs_init_data()
        self.feed_desc_stat_init_data()

    def feed_desc_stat_init_data(self):
        """Fill the data for descriptive statistics combobox"""
        data = data = self.model.get_selector_data('Origin', None)
        data.sort()
        self.view.desc_stat.val = [''] + data
        self.view.desc_stat.binder(self.insert_desc_stat_text)

    def feed_graphs_init_data(self):
        """filled the first selector of each graph with initial datas.
        And bind the plot button."""
        graphs = self.view.get_all_graphs()
        for graph in graphs:
            panel = graph.side_panel
            first_box = panel.first_selector
            self.feed_data(graph, first_box.label, None)
            panel.disable_next_selectors(first_box.label)
            panel.bind_selectors(self.selector_selected)
            panel.bind_button('PLOT', self.activate_plot)
            if panel.is_history_box:
                panel.history_box.binder(self.history_box_selected)
                panel.bind_button('ADD', self.add_to_history_box)
                panel.bind_button('REMOVE', self.remove_from_history_box)
                panel.bind_selector('Airline', self.airlines_selected)
                panel.set_button_state('PLOT', 'disabled')
                panel.set_button_state('REMOVE', 'disabled')
                self.feed_data(graph, 'Airline')
                self.feed_data(graph, 'Origin (Optional)')

    def insert_desc_stat_text(self, airline):
        """Insert descriptive statistics"""
        title = f'Average delay of flights departed from {airline} in minutes\n'
        describe = title + self.model.desc_stat_data(airline)
        self.view.desc_stat.insert_text(describe)

    def history_box_selected(self, cur_sel):
        """Enabled a remove button when historybox is selected"""
        panel = self.view.get_current_graph().side_panel
        if cur_sel in panel.history_box.values:
            panel.get_selector('Airline').set_selected(cur_sel)
            panel.set_button_state('REMOVE', 'normal')

    def airlines_selected(self, event):
        """Enabled add/remove buttons when airline is selected"""
        panel = self.view.get_current_graph().side_panel
        panel.set_button_state('REMOVE', 'disabled')
        airline = panel.get_selector_options()['Airline']
        if airline in panel.history_box.values:
            panel.set_button_state('REMOVE', 'normal')
        else:
            panel.set_button_state('ADD', 'normal')
        self.selector_selected('Airline')

    def add_to_history_box(self, event):
        """Add element to historybox"""
        panel = self.view.get_current_graph().side_panel
        airline = panel.get_selector_options()['Airline']
        if panel.get_button_state('ADD') == 'normal':
            panel.history_box.append(airline)
            panel.set_button_state('PLOT', 'normal')
            panel.set_button_state('REMOVE', 'normal')
            panel.set_button_state('ADD', 'disabled')

    def remove_from_history_box(self, event):
        """Removing element from historybox"""
        panel = self.view.get_current_graph().side_panel
        airline = panel.get_selector_options()['Airline']
        if panel.get_button_state('REMOVE') == 'normal':
            panel.history_box.remove(airline)
            panel.set_button_state('ADD', 'normal')
            panel.set_button_state('REMOVE', 'disabled')
        if not panel.history_box.values:
            panel.set_button_state('PLOT', 'disabled')

    def activate_plot(self, event):
        """Plot the graph"""
        try:
            graph = self.view.get_current_graph()
            panel = graph.side_panel
            if panel.get_button_state('PLOT') == 'normal':
                graph_name = self.view.get_current_tab_name()
                options = panel.get_selector_options()
                if panel.is_history_box:
                    options['airline'] = panel.history_box.values
                    options['compare'] = graph_name
                data, title = self.model.get_graph_data(graph_name, options)
                graph.plot_graph(data, title)
        except Exception as e:
            messagebox.showerror('Error', e)
            panel.set_button_state('PLOT', 'normal')

    def selector_selected(self, selector_name):
        """Fill the next selector with data after the first one is selected"""
        graph = self.view.get_current_graph()
        panel = graph.side_panel
        next_selector = panel.get_next_selector(selector_name)
        if next_selector:
            panel.disable_next_selectors(selector_name)
            filters = panel.get_selector_options()
            self.feed_data(graph, next_selector.label, filters)
            if panel.is_history_box:
                panel.history_box.values = []
                self.feed_data(graph, 'Airline', filters)
