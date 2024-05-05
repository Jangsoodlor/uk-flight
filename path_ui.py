import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from side_panel import SidePanel

class PathUI(tk.Frame):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.init_components()

    def init_components(self):
        self.side_panel = SidePanel(self)
        self.side_panel.pack(side='right', padx=10, pady=10)
        bg = self.side_panel.cget('bg')
        self.init_side_panel()
        self.text = ScrolledText(self, state='disabled', bg=bg)
        self.text.configure(selectbackground=bg,
                            inactiveselectbackground=bg)
        self.text.pack(fill='both', expand=True, side='left')
        self.inner_frame = tk.Frame(self.text, bg='#f0f0f0')
        self.text.window_create('1.0', window=self.inner_frame)

    def init_side_panel(self):
        self.side_panel.create_selector('Origin')
        self.side_panel.create_selector('Destination')
        self.side_panel.create_button('Find Route')

    def clear_subframes(self):
        for child in self.inner_frame.winfo_children():
            child.destroy()

    def create_subframes(self, flights):
        self.clear_subframes()
        titles = ['Origin: ',
                  'Destination: ',
                  'Airline: ',
                  'Cancellation Rate: ',
                  'Average Delay (minutes): ']
        for flight in flights:
            frm = tk.Frame(self.inner_frame)
            for i, val in enumerate(flight):
                text = titles[i] + str(val)
                label = tk.Label(frm, text=text)
                label.pack(anchor='w')
            frm.pack(anchor='w', padx=5, pady=10, fill='x', expand=True)

if __name__ == '__main__':
    import pandas as pd
    import os
    from pathfinder import Pathfinder
    origin = 'ABERDEEN'
    dest = 'JOHANNESBURG'
    df = pd.read_csv(os.path.join(os.getcwd(),
                                'data/202401_Punctuality_Statistics_Full_Analysis.csv'))
    df = df[df['number_flights_matched'] > 0]
    df.reset_index(inplace=True)
    p = Pathfinder(df)
    a = p.find_flight_path(origin, dest)

    root = tk.Tk()
    u = PathUI(root)
    u.create_subframe(a)
    u.pack(fill='both', expand=True)
    root.mainloop()
