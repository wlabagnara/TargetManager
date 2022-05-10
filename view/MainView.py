"""
    Main application view (GUI)
"""

import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import messagebox as tkmb
import pathlib as p

from matplotlib import pyplot as plt

import drawplots.DrawPlots as dp
import utils.Utils as utils

import client.KeepAlive as ka
import server.TargetSimulator as ts

import pandas as pd

class GUI(tk.Tk): 
    """ Application main GUI window derived from tkinter class."""
    def __init__(self):
        super().__init__()
        self.title('Target Manager')
        self.geometry('1000x768')
        # self.resizable(0,0) # uncomment to disable resizing of app window
        icon_image = PhotoImage(file=str(p.Path(__file__).parent.absolute()) + '\\main.png') # convert to relative path!
        self.iconphoto(False, icon_image)

        style = ttk.Style()
        style.theme_use('xpnative') # default, xpnative, winnative, vista, classic, clam, alt
        # style.configure('TLabelframe.Label', font = ('helvetica', 12, 'bold'), foreground='cyan')  
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # handle window's close icon 'X'

        # initialize client/server objects and start their threads
        self.host_ip_var = tk.StringVar()    
        self.host_udp_var = tk.StringVar()    
        self.target_ip_var = tk.StringVar()    
        self.target_udp_var = tk.StringVar()    

        self.create_panel()
        self.create_window_tabs()

        # plots in GUI frame tabs
        self.fig = plt.Figure()
        plot1 = dp.DrawPlots(self.fig, self.tab3)

        self.create_config_frame(self.tab1)
        self.create_data_view(self.tab2)



    def create_panel(self):
        """ Create a status panel to display indicators and such."""
        panel = ttk.LabelFrame(self, text="STATUS") 
        panel.rowconfigure(0, weight=1)
        panel.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        ttk.Label(panel, text="RX").grid(column=1, row=0, sticky='nesw', padx=5)
        ttk.Label(panel, text="TX").grid(column=2, row=0, sticky='nesw', padx=5)

        self.rx_sync_var = tk.StringVar()
        self.rx_sync_var.set("--")
        self.rx_sync_lbl = ttk.Label(panel, background='red', foreground='white', textvariable=self.rx_sync_var)
        self.rx_sync_lbl.grid(column=1, row=1, sticky='nesw', padx=5, pady=2)

        self.tx_sync_var = tk.StringVar()
        self.tx_sync_var.set("--")
        self.tx_sync_lbl = ttk.Label(panel, background='blue', foreground='white', textvariable=self.tx_sync_var)
        self.tx_sync_lbl.grid(column=2, row=1, sticky='nesw', padx=5, pady=2)

        panel.bind("<Enter>", self.on_enter) # tool-tip help
        panel.bind("<Leave>", self.on_leave)
        self.help_var = tk.StringVar()
        self.help_var.set(" ")
        help_lbl = ttk.Label(self, textvariable=self.help_var, foreground='dark orange')
        help_lbl.configure( font=('Consolas', 10, 'italic'))
        help_lbl.grid(column=0, row=99, sticky=tk.NSEW, padx=10, pady=10)

    def create_window_tabs(self):
        """ Create a set of window tab views. """
        nb = ttk.Notebook(self)
        nb.grid(column=0, row=3, sticky=tk.N+tk.E+tk.W+tk.S, padx=5, pady=5)
        nb.enable_traversal() # can use arrow keys to switch tabs
        # create first tabs frame 
        self.tab1 = ttk.Frame(nb) # use this frame to put objects under this tab
        nb.add(self.tab1, text='Configuraton ', underline=0, padding=5)
        # create second tabs frame
        self.tab2 = ttk.Frame(nb) # use this frame to put objects under this tab
        nb.add(self.tab2, text='Data  ', underline=0, padding=5)
        # create third tabs frame
        self.tab3 = ttk.Frame(nb) # use this frame to put objects under this tab
        nb.add(self.tab3, text='Plots  ', underline=0, padding=5)
        # create fourth tabs frame
        self.tab4 = ttk.Frame(nb) # use this frame to put objects under this tab
        nb.add(self.tab4, text='More  ', underline=0, padding=5)

    def set_default_network_config(self):
        self.target_ip_var.set("localhost")
        self.target_udp_var.set("5005")
        self.host_ip_var.set("localhost")
        self.host_udp_var.set("5005")

        df = pd.DataFrame({
            'Host':[self.host_ip_var.get(), self.host_udp_var.get()],
            'Target':[self.target_ip_var.get(), self.target_udp_var.get()]
        })

        df.to_json("network_config.json")
        read_f = pd.read_json("network_config.json")
        return read_f

    def save_network_config(self):
        """ Save the network configuration to a file"""
        df = pd.DataFrame({
            'Host':[self.host_ip_var.get(), self.host_udp_var.get()],
            'Target':[self.target_ip_var.get(), self.target_udp_var.get()]
        })

        df.to_json("network_config.json")
        print(f'Saved network config file host: {self.host_ip_var.get()} {self.host_udp_var.get()} target: {self.target_ip_var.get()} {self.target_udp_var.get()}')

    def read_network_config(self):
        """ Read the network configuration from a file """
        
        try:
            read_f = pd.read_json("network_config.json")
        except:
            print(f"Network configuration does not exist, so create default settings file.")
            read_f = self.set_default_network_config()

        host_ip = read_f['Host'][0]
        host_udp = read_f['Host'][1]
        target_ip = read_f['Target'][0]
        target_udp = read_f['Target'][1]
        print(f'Read network config file -- host: {host_ip} {host_udp} target: {target_ip} {target_udp}')
        return (host_ip, host_udp, target_ip, target_udp)

    def create_config_frame(self, tab):
        """ Create a view for the configuration items."""

        nc = self.read_network_config()
        
        self.host_ip_var.set(nc[0])
        self.host_udp_var.set(nc[1])
        self.target_ip_var.set(nc[2])
        self.target_udp_var.set(nc[3])

        self.server = ts.TargetSimulator(self.target_ip_var.get(), int(self.target_udp_var.get())) 
        self.client = ka.KeepAlive(self.host_ip_var.get(), int(self.host_udp_var.get()), "Hello Worldlings!")    
        self.start_threads()
    
        self.config = ttk.LabelFrame(tab, text="Network Configuration") 
        
        self.config.columnconfigure(0, weight=1)
        self.config.columnconfigure(1, weight=10)
        self.config.columnconfigure(2, weight=1)
        self.config.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        frm_width = 80

        ttk.Label(self.config, text='Host IP Address:  ').grid(column=0, row=0, sticky=tk.W)
        ttk.Entry(self.config, textvariable=self.host_ip_var, width=frm_width).grid(column=1, row=0, sticky=tk.W)

        ttk.Label(self.config, text='Host UDP Port:  ').grid(column=0, row=1, sticky=tk.W)
        ttk.Entry(self.config, textvariable=self.host_udp_var, width=frm_width).grid(column=1, row=1, sticky=tk.W)

        ttk.Label(self.config, text='Target IP Address:  ').grid(column=0, row=2, sticky=tk.W)
        ttk.Entry(self.config, textvariable=self.target_ip_var, width=frm_width).grid(column=1, row=2, sticky=tk.W)

        ttk.Label(self.config, text='Target UDP Port:  ').grid(column=0, row=3, sticky=tk.W)
        ttk.Entry(self.config, textvariable=self.target_udp_var, width=frm_width).grid(column=1, row=3, sticky=tk.W)

        ttk.Button(self.config, text='Save Configuration', command=self.save_network_config).grid(column=0, row=4, sticky='nesw')

    def create_data_view(self, tab):
        """ Create a text window for displaying captured data and such. """
        self.body = ttk.Frame(tab)
        self.data = tk.Text(self.body, height=20)
        self.data.grid(column=0, row=1)
        scrollbar = ttk.Scrollbar(self.body, orient='vertical', command=self.data.yview)
        scrollbar.grid(column=1, row=1, sticky=tk.NS)
        self.data['yscrollcommand'] = scrollbar.set
        self.body.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

    def check_status(self):
        """ Poll the various status information for GUI presentation."""
        self.rx_sync_var.set(str(self.client.get_rx_msg_rate())) 
        self.tx_sync_var.set(str(self.client.get_tx_msg_rate())) 

        while self.client.rx_data_avail(): # will 'block' in loop until queue is 'drained'
            msg = self.client.get_rx_data() + '\n'
            self.data.insert('1.0', msg)

        if self.client.get_rx_sync() == True:
            self.rx_sync_lbl.config(background='green')
        else:
            self.rx_sync_lbl.config(background='red')

        self.after(1000, self.check_status) # poll for status changes every second

    def start_threads(self):
        """ Start the threads required for the main application."""
        self.check_status()
        self.client.start() # start server then client thread
        self.server.start()

    def exit_app(self):
        """ Cleanly exit the main application."""
        self.client.stop() # stop threads
        self.server.stop()
        self.destroy() # quit GUI
        print(f"Exiting application!")
        import os  
        os._exit(0)

    def on_closing(self):
        """ Kindly close the main application window."""
        if tkmb.askokcancel("Are you sure?", "Do you really want to quit?") == True:
            self.exit_app()

    """ Tooltip help methods. Displays tip when you hover over something."""
    def on_enter(self, enter):
        self.help_var.set("TIP: RX and TX are rates in messages/second. RX red is OOS, green is INSYNC; TX is always blue.")
        
    def on_leave(self, event):
        self.help_var.set(" ")

