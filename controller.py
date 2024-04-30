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
        data_method = {'Airport':self.model.get_airport_name}
        for graph in self.view.graphs.values():
            combobox_name = graph.get_first_combobox
            data = data_method[combobox_name]()
            graph.side_panel.set_selector_value(combobox_name, data)
            graph.side_panel.get_selector(combobox_name).set_state('normal')


if __name__ == '__main__':
    import os
    import pandas as pd
    df = pd.read_csv(os.path.join(os.getcwd(),
                                  'data/202401_Punctuality_Statistics_Full_Analysis.csv'))
    m = Model(df)
    v = TabManager()
    c = Controller(v,m)
    c.run()
