"""UI for Find Flight Route tab"""
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
from PIL import Image, ImageTk
from side_panel import SidePanel


class PathUI(tk.Frame):
    """UI for Find Flight Route tab"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.init_components()

    def init_components(self):
        """Initialise components"""
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
        """Initialise side panel"""
        self.side_panel.create_selector('Origin')
        self.side_panel.create_selector('Destination')
        self.side_panel.create_button('Find Route')

    def clear_subframes(self):
        """Clear the display"""
        for child in self.inner_frame.winfo_children():
            child.destroy()

    def create_subframes(self, flights):
        """Create subframse for the display. A subframe includes the
        information of the flight, as well as the logo of the airline."""
        self.clear_subframes()
        if None in flights:
            lab = tk.Label(self.inner_frame, text='No Flights Exists')
            lab.pack(anchor='w', pady=10, fill='both', expand=True)
        else:
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
        """Read the logo and append it to the subframe"""
        image_path = os.path.join(os.getcwd(), f'logo/{airline}.png')
        image = ImageTk.PhotoImage(Image.open(image_path))
        image_label = tk.Label(frm, image=image)
        image_label.image = image
        image_label.pack(side='left', fill='both', expand=True)

    def __make_description(self, frm, flight):
        """Creates a description of a flight and append it to the subframe"""
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
