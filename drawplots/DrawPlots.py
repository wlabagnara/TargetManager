from matplotlib import pyplot as plt
import matplotlib.animation as ani
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import tkinter as tk

import pandas as pd

class DrawPlots(tk.Tk): 
    def __init__(self, fig, tab):
        self.fig = fig
        self.ax = self.fig.add_subplot(111)
        self.tab = tab
        self.animate() # update plots every tick

    def update(self, i):
        """ Create a plot of real-time data """
        data = pd.read_csv('sim_data.csv')
        x = data['x_value']
        y1 = data['total_1']
        self.ax.cla() 
        ## plt.style.use('fivethirtyeight') # makes plots nicer
        ## plt.style.use('seaborn')
        ## plt.style.use('ggplot')

        self.ax.plot(x, y1, label='Channel 1')
        self.ax.grid()
        self.ax.legend(loc='upper left')
        self.toobar = NavigationToolbar2Tk(self.line2, self.tab, pack_toolbar=False)
        self.toobar.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)    

    def animate(self):
        self.line2 = FigureCanvasTkAgg(self.fig, self.tab)                                     
        self.line2.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        self.ani = ani.FuncAnimation(self.fig, self.update, interval=1000)