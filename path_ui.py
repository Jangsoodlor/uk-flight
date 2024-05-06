import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
from PIL import Image, ImageTk
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
        self.text.pack(fill='both', expand=True, anchor='w')
        self.inner_frame = tk.Frame(self.text)
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

        for flight in flights:
            frm = tk.Frame(self.inner_frame)
            frm_img = tk.Frame(frm)
            self.__make_logo(frm_img, flight[0])
            frm_img.pack(side='left', anchor='w', padx=20)

            frm_text = tk.Frame(frm)
            self.__make_description(frm_text, flight)
            frm_text.pack(side='right', fill='both', expand=True)
            frm.pack(anchor='w', pady=10, fill='both', expand=True)

    def __make_logo(self, frm, airline):
        image_path = os.path.join(os.getcwd(), f'logo/{airline}.png')
        image = ImageTk.PhotoImage(Image.open(image_path))
        image_label = tk.Label(frm, image=image)
        image_label.image = image
        image_label.pack(side='left', fill='both', expand=True)

    def __make_description(self, frm, flight):
        titles = ['',
                  'Origin: ',
                  'Destination: ',
                  'Cancellation Rate: ',
                  'Average Delay: ']

        for i, val in enumerate(flight):
            text = titles[i] + str(val)
            if i == 3:
                text += ' %'
            elif i == 4:
                text += ' minutes'
            label = tk.Label(frm, text=text)
            if i == 0:
                label.config(font=('Arial', 15))
            label.pack(anchor='w')

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
