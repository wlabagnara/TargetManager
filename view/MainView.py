"""
    Main application view (GUI)
"""

import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter.messagebox import showerror

class GUI(tk.Tk): # application main window derived from tkinter GUI class
    def __init__(self):
        super().__init__()
        self.title('Target Manager')
        self.geometry('680x430')
        self.resizable(0,0) # disable resizing
        pl = PhotoImage(file='C:/Projects/TargetManager/view/main.png') # convert to relative path!
        self.iconphoto(False, pl)
        self.create_header_frame()
        self.create_body_frame()
        self.create_footer_frame()

    def create_header_frame(self):
        self.header = ttk.Frame(self)
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

    def create_body_frame(self):
        self.body = ttk.Frame(self)
        self.html = tk.Text(self.body, height=20)
        self.html.grid(column=0, row=1)
        scrollbar = ttk.Scrollbar(self.body, orient='vertical', command=self.html.yview)
        scrollbar.grid(column=1, row=1, sticky=tk.NS)
        self.html['yscrollcommand'] = scrollbar.set
        self.body.grid(column=0, row=1, sticky=tk.NSEW, padx=10, pady=10)

    def create_footer_frame(self):
        self.footer = ttk.Frame(self)
        self.footer.columnconfigure(0, weight=1)
        self.exit_button = ttk.Button(self.footer, text='Exit', command=self.destroy)
        self.exit_button.grid(column=0, row=0, sticky=tk.E)
        self.footer.grid(column=0, row=2, sticky=tk.NSEW, padx=10, pady=10)

## MAIN APP TESTING
if __name__ == "__main__":
    
    app = GUI()
    app.mainloop()
