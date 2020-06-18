from tkinter import *
from tkinter import ttk

import requests

APIKEY = 'facf808d'
URL = 'http://www.omdbapi.com/?s={}&apikey={}'

class Searcher (ttk.Frame):
    def __init__(self, parent, command):
        ttk.Frame.__init__(self, parent,)

        lblSearcher = ttk.Label (self, text='Film:')
        self.ctrSearcher = StringVar ()
        txtSearcher = ttk.Entry(self, width=30, textvariable=self.ctrSearcher)
        btnSearcher = ttk.Button(self, text='Search', command=lambda:command(self.ctrSearcher.get()))

        lblSearcher.pack(side=LEFT)
        txtSearcher.pack(side=LEFT)
        btnSearcher.pack(side=LEFT)

    def click (self):
        print(self.ctrSearcher.get())

class Controller (ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=300, height=400)
        self.grid_propagate(False)

        self.searcher=Searcher(self, self.busca)
        self.searcher.grid(column=0, row=0)

    def busca(self, peli):
        print (peli)

        url=URL.format(peli, APIKEY)
        results = requests.get(url)

        print (results.text)

       

