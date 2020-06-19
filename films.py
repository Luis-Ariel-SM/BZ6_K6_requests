from tkinter import *
from tkinter import ttk
from configparser import * # LIbreria para procesar los config.ini con python

import requests

config=ConfigParser() # Instanciando ConfigParser
config.read('config.ini') # Abriendo nuestro fichero config.ini
APIKEY = config['OMDB_API']['APIKEY'] # Leyendo la apikey que se encuentra guardada en el fichero config.ini

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

        self.film = Film (self)
        self.film.grid(column=0, row=1)

    def busca(self, peli):
        print (peli)

        url=URL.format(peli, APIKEY)
        results = requests.get(url)

        if results.status_code==200:
            films=results.json() # Convirtiendo cadena en diccionario segun la sintaxis del modulo requests
            if films.get('Response')=='True':
                first_film=films.get('Search')[0]
                mi_peli = {'titulo': first_film.get('Title'), 'año': first_film.get ('Year'), 'poster': first_film.get('Poster')}
                self.film.encontrada = mi_peli
        else:
            pass

        print (results.text)

class Film (ttk.Frame):
    __encontrada = None
   
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.lblTitle = ttk.Label(self, text='Titulo')
        self.lblYear = ttk.Label(self, text = '1900')

        self.lblTitle.pack(side=TOP)
        self.lblYear.pack(side=TOP)
       
    @property
    def encontrada (self):
        return self.__encontrada

    @encontrada.setter
    def encontrada (self, value):
        self.__encontrada = value

        self.lblTitle.config(text=self.__encontrada.get ('titulo'))
        self.lblYear.config(text=self.__encontrada.get ('año'))

