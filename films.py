from tkinter import *
from tkinter import ttk
from configparser import * # LIbreria para procesar los config.ini con python

import requests

from PIL import Image, ImageTk
from io import BytesIO

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
        ttk.Frame.__init__(self, parent, width=305, height=550)
        self.grid_propagate(False) # Si le pones un True la pantalla adopta el tamaños automatico de lo que tenga, es una buena opcion igual

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
        self.image = Label(self)
        self.photo = None

        self.image.pack (side=TOP)
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

        if self.__encontrada.get('poster')=='N/A':
            return
        r = requests.get (self.__encontrada.get('poster')) # Recupero la imagen de internet
        if r.status_code == 200:
            bin_image = r.content # Transformando la imagen en binario segun metodo del modulo requests (Aun python no lo entiende)
            image = Image.open(BytesIO(bin_image)) # Sintaxis para que Python entienda los binarios de imagenes o musica utilizando los modulos especificos para esto
            self.photo = ImageTk.PhotoImage(image) # Tranformando la imagen para que ahora la entienda tkinter 

            self.image.config(image=self.photo)
            self.image.image = self.photo

