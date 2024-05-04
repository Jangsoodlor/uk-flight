from tkinter import messagebox

class Controller:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.feed_init_data()

    def run(self):
        """Run the app"""
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
            graph.side_panel.bind_button('PLOT', self.activate_plot)
            if graph.side_panel.is_history_box:
                graph.side_panel.history_box.bind(self.history_box_selected)
                graph.side_panel.bind_button('ADD', self.add_to_history_box)
                graph.side_panel.bind_button('REMOVE', self.remove_from_history_box)
                graph.side_panel.bind_selector('Airline', self.airlines_selected)
                graph.side_panel.set_button_state('PLOT', 'disabled')
                graph.side_panel.set_button_state('REMOVE', 'disabled')
                self.always_active_selector(graph, 'Airline')           
                self.always_active_selector(graph, 'Origin (Optional)')           

    def always_active_selector(self, graph, name, filters=None):
        selector =  graph.side_panel.get_selector(name)
        data = self.model.get_selector_data(selector.label, filters)
        selector.val = data

    def history_box_selected(self, cur_sel):
        graph = self.view.get_current_graph()
        if cur_sel in graph.side_panel.history_box.values:
            graph.side_panel.get_selector('Airline').set_selected(cur_sel)
            graph.side_panel.set_button_state('REMOVE', 'normal')

    def airlines_selected(self, event):
        graph = self.view.get_current_graph()
        graph.side_panel.set_button_state('REMOVE', 'disabled')
        airline = graph.side_panel.get_selector_options()['Airline']
        if airline in graph.side_panel.history_box.values:
            graph.side_panel.set_button_state('REMOVE', 'normal')
        else:
            graph.side_panel.set_button_state('ADD', 'normal')
        self.selector_selected('Airline')

    def add_to_history_box(self, event):
        #TODO Add if else
        panel = self.view.get_current_graph().side_panel
        airline = panel.get_selector_options()['Airline']
        if panel.get_button_state('ADD') == 'normal':
            panel.history_box.append(airline)
            panel.set_button_state('PLOT', 'normal')
            panel.set_button_state('REMOVE', 'normal')
            panel.set_button_state('ADD', 'disabled')

    def remove_from_history_box(self, event):
        panel = self.view.get_current_graph().side_panel
        airline = panel.get_selector_options()['Airline']
        if panel.get_button_state('REMOVE') == 'normal':
            panel.history_box.remove(airline)
            panel.set_button_state('ADD', 'normal')
            panel.set_button_state('REMOVE', 'disabled')
        if not panel.history_box.values:
            panel.set_button_state('PLOT', 'disabled')

    def activate_plot(self, event):
        try:
            graph = self.view.get_current_graph()
            if graph.side_panel.get_button_state('PLOT') == 'normal':
                graph_name = self.view.get_current_tab_name()
                options = graph.side_panel.get_selector_options()
                if graph.side_panel.is_history_box:
                    options['airline'] = graph.side_panel.history_box.values
                    options['compare'] = graph_name
                data, title = self.model.get_graph_data(graph_name, options)
                graph.plot_graph(data, title)
        except Exception as e:
            messagebox.showerror('Error', e)


    def selector_selected(self, selector_name):
        """Fill the next selector with data after the first one is selected"""
        current_graph = self.view.get_current_graph()
        next_selector = current_graph.side_panel.get_next_selector(selector_name)
        if next_selector:
            current_graph.side_panel.disable_next_selectors(selector_name)
            filters = current_graph.side_panel.get_selector_options()
            data = self.model.get_selector_data(next_selector.label, filters)
            next_selector.val = data
            if current_graph.side_panel.is_history_box:
                current_graph.side_panel.history_box.values = []
                self.always_active_selector(current_graph, 'Airline', filters)
