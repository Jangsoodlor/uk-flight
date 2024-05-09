"""The controller. Which controls interaction between view and model"""
from tkinter import messagebox
from pathfinder import Pathfinder

class Controller:
    """The Controller class"""
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.pathfinder = None
        self.feed_init_data()

    def run(self):
        """Run the app"""
        self.view.run()

    def feed_data(self, selector, filters=None):
        """Set the data of a certain combobox in a specific graph"""
        data = self.model.get_selector_data(selector.label, filters)
        data.sort()
        selector.val = [''] + data

    def feed_init_data(self):
        """Fill the first selectors of each tab with initial data"""
        self.view.bind_tab_selected(self.tab_selected)
        self.feed_graphs_init_data()
        self.feed_desc_stat_init_data()
        self.feed_pathfinder_init_data()

    def tab_selected(self, name):
        if name == 'Data Storytelling':
            self.display_storytelling()

    def feed_desc_stat_init_data(self):
        """Fill the data for descriptive statistics combobox"""
        data = data = self.model.get_selector_data('Origin', None)
        data.sort()
        self.view.desc_stat.val = [''] + data
        self.view.desc_stat.binder(self.insert_desc_stat_text)

    def feed_pathfinder_init_data(self):
        side_panel = self.view.path_ui.side_panel
        for selector in side_panel:
            self.feed_data(selector)
        side_panel.bind_button('Find Route', self.find_route)

    def find_route(self, event):
        try:
            options = self.view.path_ui.side_panel.get_selector_options()
            if not self.pathfinder:
                self.pathfinder = Pathfinder(self.model.df)
            flights = self.pathfinder.find_flight_path(options['Origin'], options['Destination'])
            self.view.path_ui.create_subframes(flights)
        except ValueError as v:
            messagebox.showerror('Error', v)

    def display_storytelling(self):
        """Displays the story telling tab"""
        datas = self.model.data_storytelling()
        self.view.storytelling.plot_graph(datas)

    def insert_desc_stat_text(self, airline):
        """Insert descriptive statistics"""
        title = f'Average delay of flights departed from {airline} in minutes\n'
        describe = title + self.model.desc_stat_data(airline)[:-40]
        self.view.desc_stat.insert_text(describe)

    def feed_graphs_init_data(self):
        """filled the first selector of each graph with initial datas.
        And bind the plot button."""
        graphs = self.view.get_all_graphs()
        for graph in graphs:
            panel = graph.side_panel
            first_box = panel.first_selector
            self.feed_data(first_box)
            panel.disable_next_selectors(first_box.label)
            panel.bind_selectors(self.selector_selected)
            if panel.has_history_box:
                panel.history_box.binder(self.history_box_selected)
                panel.bind_button('ADD', self.add_to_history_box)
                panel.bind_button('REMOVE', self.remove_from_history_box)
                panel.bind_selector('Airline', self.airlines_selected)
                # panel.set_button_state('PLOT', 'disabled')
                panel.set_button_state('REMOVE', 'disabled')
                self.feed_data(panel.get_selector('Airline'))
                self.feed_data(panel.get_selector('Origin (Optional)'))
            else:
                panel.bind_button('PLOT', self.activate_plot)

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
            panel.set_button_state('REMOVE', 'normal')
            panel.set_button_state('ADD', 'disabled')
            self.activate_plot(None)

    def remove_from_history_box(self, event):
        """Removing element from historybox"""
        panel = self.view.get_current_graph().side_panel
        airline = panel.get_selector_options()['Airline']
        if panel.get_button_state('REMOVE') == 'normal':
            panel.history_box.remove(airline)
            panel.set_button_state('ADD', 'normal')
            panel.set_button_state('REMOVE', 'disabled')
        if panel.history_box.values:
            self.activate_plot(None)

    def activate_plot(self, event):
        """Plot the graph"""
        try:
            graph = self.view.get_current_graph()
            panel = graph.side_panel
            if panel.get_button_state('PLOT') == 'normal':
                graph_name = self.view.get_current_tab_name()
                options = panel.get_selector_options()
                if panel.has_history_box:
                    options['airline'] = panel.history_box.values
                    options['compare'] = graph_name
                data, title = self.model.get_graph_data(graph_name, options)
                graph.plot_graph(data, title)
        except Exception as e:
            messagebox.showerror('Error', e)

    def selector_selected(self, selector_name):
        """Fill the next selector with data after the first one is selected"""
        panel = self.view.get_current_graph().side_panel
        next_selector = panel.get_next_selector(selector_name)
        if next_selector:
            panel.disable_next_selectors(selector_name)
            filters = panel.get_selector_options()
            self.feed_data(next_selector, filters)
            if panel.has_history_box:
                panel.history_box.values = []
                panel.set_button_state('ADD', 'disabled')
                panel.set_button_state('REMOVE', 'disabled')
                self.feed_data(panel.get_selector('Airline'), filters)
