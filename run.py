#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import demjson
from Tkinter import *
from ttk import Style
import tkMessageBox as box
import tkFileDialog
import pandas as pd
from optionchain import *

class Gui(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        self.parent = parent
        self.file_opt = options = {}
        options['filetypes'] = [('excel files', '.xls'),]
        options['initialfile'] = 'option_chains.xls'
        self.initUI()
        self.createWidgets()
    
    def initUI(self):
        self.parent.title("Google Finance Option Chain")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
    

    def createWidgets(self):
        self.text_entry = Entry(self)
        self.text_entry["width"] = 23
        self.text_entry.insert(0, "NASDAQ:AAPL")
        self.text_entry.pack({"side": "top",'pady':10,'padx':15})

        self.download_btn = Button(self)
        self.download_btn["text"] = "Download Option Chain"
        self.download_btn["command"] = self.submit
        self.download_btn["width"] = 20
        self.download_btn.pack({"side": "top",'pady':10,'padx':15})

        self.quit_btn = Button(self)
        self.quit_btn["text"] = "Exit"
        self.quit_btn["command"] =  self.quit
        self.quit_btn["width"] = 20
        self.quit_btn.pack({"side": "top",'pady':10,'padx':15})
        
    def submit(self):
        if len(self.text_entry.get()) > 0:
            self.chain_query = self.text_entry.get()
            self.init_option_chain()
        else:
            box.showerror("Error", "Entry should not be empty")

    """
        Initialize and retrieve OptionChain base on argument needed i.e 'q' 
    """
    def init_option_chain(self):
        self.df = df = {}
        self.optionchain = OptionChain(self.chain_query)
        if self.optionchain.retrieve_success:
            df['calls'] = pd.DataFrame(data=self.optionchain.get_all_options('calls'))
            df['puts'] = pd.DataFrame(data=self.optionchain.get_all_options('puts'))
            self.download_btn["text"] = "Export Option Chain"
            self.download_btn["command"] = self.export_option_chain
        else: 
            box.showerror("Error", "Unable to retrieve data from source.")

    """
        Export retrieved option chains in individual spreadsheets
    """
    def export_option_chain(self):
        filename = tkFileDialog.asksaveasfilename(**self.file_opt)
        writer = pd.ExcelWriter(filename)
        self.df['calls'].to_excel(writer, 'calls')
        self.df['puts'].to_excel(writer, 'puts')
        writer.save()

    def view_pd_data(self):
        print self.df['calls']
        print self.df['puts']

def main():
  
    root = Tk()
    app = Gui(root)
    root.mainloop()  

if __name__ == '__main__':
    main()  