from tkinter import *
from tkinter import ttk

import films

class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Busca peliculas')
        searcher = films.Controller(self)
        searcher.pack()

    def main (self):
        self.mainloop()

if __name__ == '__main__':
    app = MainApp()
    app.main()
