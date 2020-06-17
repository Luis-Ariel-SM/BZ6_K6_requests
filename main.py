import requests

URL = 'http://www.omdbapi.com/?s={}&apikey=facf808d'

peli = input ('Buscar: ')

respuesta = requests.get(URL.format(peli)) # Se puede meter la url directamente en el parentesis igual

# print (respuesta.text)

mijson = respuesta.json() # Para cambiar una cadena a Json la diferencia se nota en las comillas sencillas porque asi es como json 
# interpreta las cadenas. Ademas con el debug se ve como el json es un diccionario

print (mijson.get ('Search')[0].get('Title'))
print (mijson.get ('Search')[0].get('Poster'))