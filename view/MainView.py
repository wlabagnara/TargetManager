"""
    Main application view (GUI)
"""

import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import messagebox as tkmb
import pathlib as p


class GUI(tk.Tk): # application main window derived from tkinter GUI class
    def __init__(self, client, server):
        super().__init__()
        self.title('Target Manager')
        self.geometry('800x600')
        self.resizable(0,0) # uncomment to disable resizing of app window
        icon_image = PhotoImage(file=str(p.Path(__file__).parent.absolute()) + '\\main.png') # convert to relative path!
        self.iconphoto(False, icon_image)

        style = ttk.Style()
        style.theme_use('xpnative') # default, xpnative, winnative, vista, classic, clam, alt
        # style.configure('TLabelframe.Label', font = ('helvetica', 12, 'bold'), foreground='cyan')  
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # handle window's close icon 'X'

        self.create_panel()
        self.create_window_tabs()
        self.create_config_frame(self.frm1)
        self.create_data_view(self.frm2)

        # initialize client/server objects and start their threads
        self.client = client
        self.server = server
        self.start_threads()

    def create_panel(self):
        
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
        # create a notebook to have window tabs
        nb = ttk.Notebook(self)
        nb.grid(column=0, row=3, sticky=tk.N+tk.E+tk.W+tk.S, padx=5, pady=5)
        nb.enable_traversal() # can use arrow keys to switch tabs
        # create first tabs frame 
        self.frm1 = ttk.Frame(nb) # use this frame to put objects under this tab
        nb.add(self.frm1, text='Configuraton ', underline=0, padding=5)
        # create second tabs frame
        self.frm2 = ttk.Frame(nb) # use this frame to put objects under this tab
        nb.add(self.frm2, text='Data  ', underline=0, padding=5)

    def create_data_view(self, tab):
        self.body = ttk.Frame(tab)
        self.data = tk.Text(self.body, height=20)
        self.data.grid(column=0, row=1)
        scrollbar = ttk.Scrollbar(self.body, orient='vertical', command=self.data.yview)
        scrollbar.grid(column=1, row=1, sticky=tk.NS)
        self.data['yscrollcommand'] = scrollbar.set
        self.body.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

    def start_threads(self):
        self.check_status()
        self.client.start() # start server then client thread
        self.server.start()

    def exit_app(self):
        self.client.stop() # stop threads
        self.server.stop()
        self.destroy() # quit GUI

    def on_closing(self):
        if tkmb.askokcancel("Are you sure?", "Do you really want to quit?") == True:
            self.exit_app()

    def check_status(self):
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

    def create_config_frame(self, tab):
        self.config = ttk.LabelFrame(tab, text="IP Configuration") 
        
        self.config.columnconfigure(0, weight=1)
        self.config.columnconfigure(1, weight=10)
        self.config.columnconfigure(2, weight=1)
        self.config.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

        ttk.Label(self.config, text='Host IP Address:  ').grid(column=0, row=0, sticky=tk.W)
        self.host_ip_var = tk.StringVar()    
        self.host_ip_var.set("localhost")
        ttk.Entry(self.config, textvariable=self.host_ip_var, width=80).grid(column=1, row=0, sticky=tk.W)

        ttk.Label(self.config, text='Host UDP Port:  ').grid(column=0, row=1, sticky=tk.W)
        self.host_udp_var = tk.StringVar()    
        self.host_udp_var.set("5005")
        ttk.Entry(self.config, textvariable=self.host_udp_var, width=80).grid(column=1, row=1, sticky=tk.W)

        self.sim_en_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.config, variable=self.sim_en_var, text='Simulate Target?').grid(column=0, row=2, sticky=tk.W)

    # tool tip help methods
    def on_enter(self, enter):
        self.help_var.set("TIP: RX and TX are rates in messages/second. RX red is OOS, green is INSYNC; TX is always blue.")
        
    def on_leave(self, event):
        self.help_var.set(" ")

    ############################################
    
    def create_header_frame(self, tab):
        self.header = ttk.Frame(tab) 
        # grid
        self.header.columnconfigure(0, weight=1)
        self.header.columnconfigure(1, weight=10)
        self.header.columnconfigure(2, weight=1)
        # label
        self.label = ttk.Label(self.header, text='URL')
        self.label.grid(column=0, row=0, sticky=tk.W)
        # entry
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.header, textvariable=self.url_var, width=80)
        self.url_entry.grid(column=1, row=0, sticky=tk.EW)
        # download button
        self.download_button = ttk.Button(self.header, text='Download')
        # self.download_button['command'] = self.handle_download
        self.download_button.grid(column=2, row=0, sticky=tk.E)
        # attach header frame
        self.header.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)

    def create_body_frame(self, tab):
        self.body = ttk.Frame(tab)
        self.html = tk.Text(self.body, height=20)
        self.html.grid(column=0, row=1)
        scrollbar = ttk.Scrollbar(self.body, orient='vertical', command=self.html.yview)
        scrollbar.grid(column=1, row=1, sticky=tk.NS)
        self.html['yscrollcommand'] = scrollbar.set
        self.body.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

    def create_footer_frame(self, tab):
        self.footer = ttk.Frame(tab)
        self.footer.columnconfigure(0, weight=1)
        self.exit_button = ttk.Button(self.footer, text='Exit', command=self.exit_app)
        self.exit_button.grid(column=0, row=0, sticky=tk.E)
        self.footer.grid(column=0, row=2, sticky=tk.NSEW, padx=10, pady=10)
