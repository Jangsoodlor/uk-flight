import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from model import Model
import pandas as pd


class UI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('UK Flight')
        self.init_components()

    def init_components(self):
        tab_controller = ttk.Notebook(self)
        

    def run(self):
        self.mainloop()

if __name__ == '__main__':
    a = UI()
    a.run()

    # data = pd.DataFrame({
    #     'Python': [11.27,69],
    #     'C': [2,3],
    #     'Java': [10.46,2],
    #     'C++': [7.5,1],
    #     'C#': [5.26,3]
    # })
    # fig, ax = plt.subplots(figsize=(3,3))
    # canvas = FigureCanvasTkAgg(fig, self)
    # sns.barplot(data=data)
    # canvas.get_tk_widget().pack()
