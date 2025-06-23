import requests
from bs4 import BeautifulSoup ### Necessary for web scraping

url = 'https://dockerlabs.es/'
respuesta = requests.get(url)
if respuesta.status_code == 200: ### Validación de código 200
    soup = BeautifulSoup(respuesta.text, 'html.parser') ### Convierte toda la respuesta de la web con un parser, para poder apuntar a cualquier objeto especifico

    maquinas = soup.find_all('div', onclick=True) ### Filtra para aquellos divs, donde la acción onclick sea verdadera

    for maquina in maquinas: ### Bucle para iterar la acción para cada maquina
        onclick_text = maquina['onclick'] ### Extrae todas las instancias del arreglo maquinas, donde se tenga onclick
        nombre_maquina = onclick_text.split("'")[1] ### Extraemos el nombre, que para este caso por la estructura de la página analizada, está en la posición 1
        print(nombre_maquina)
else: ### Condicional de error
    print(f"ERROR {respuesta.status_code} en la request") ### Mensaje de error