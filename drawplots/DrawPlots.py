"""
    Draw plots for display on GUI

    Constructed with figure and display tab given by main GUI
"""

# from matplotlib import pyplot as plt
import matplotlib.animation as ani
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import tkinter as tk

import pandas as pd

class DrawPlots(tk.Tk): 
    """ Class used to animate plots on GUI from file data """
    def __init__(self, fig, tab):
        """ Works fine from command line, BUT when
            Running in VS CODE from debug...
              UserWarning: Animation was deleted without rendering anything. This is most likely not intended. 
              To prevent deletion, assign the Animation to a variable, e.g. `anim`, that exists until you have 
              outputted the Animation using `plt.show()` or `anim.save()`.
            SOLUTION: when instantiating w/i a class, do so as:
             "self.<whatever> = dp.DrawPlots(<figref>, <tabref>)"
        """    
        self.fig = fig
        self.ax = fig.add_subplot(111)
        self.tab = tab
        self.animate() # update plots every tick

    def update(self, i):
        """ Create a plot of real-time data """
        data = pd.read_csv('sim_data.csv')
        x = data['x_value']
        y1 = data['total_1']
        self.ax.cla() 

        self.ax.plot(x, y1, label='Channel 1')
        self.ax.grid()
        self.ax.legend(loc='upper left')
        self.toobar = NavigationToolbar2Tk(self.line2, self.tab, pack_toolbar=False)
        self.toobar.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)    

    def animate(self):
        """ Animate data on display based on update function """

        self.line2 = FigureCanvasTkAgg(self.fig, self.tab)                                     
        self.line2.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        self.anim = ani.FuncAnimation(self.fig, self.update, interval=1000)
