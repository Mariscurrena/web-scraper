import requests
import time
from pyfiglet import Figlet
from bs4 import BeautifulSoup ### Necessary for web scraping

url = 'https://dockerlabs.es/'
respuesta = requests.get(url)
lista_muy_facil = []
lista_facil = []
lista_medio = []
lista_dificil = []
contador = 0

class colors():
    blue = "\033[34m"
    green = "\033[32m"
    orange = "\033[38;5;208m"
    red = "\033[31m"
    purple = "\033[35m"
    end = "\033[0m"

def main(contador):
    inicio()  
    time.sleep(2)
    if respuesta.status_code == 200: ### Validación de código 200
        soup = BeautifulSoup(respuesta.text, 'html.parser') ### Convierte toda la respuesta de la web con un parser, para poder apuntar a cualquier objeto especifico
        maquinas = soup.find_all('div', onclick=True) ### Filtra para aquellos divs, donde la acción onclick sea verdadera

        for maquina in maquinas: ### Bucle para iterar la acción para cada maquina
            onclick_text = maquina['onclick'] ### Extrae todas las instancias del arreglo maquinas, donde se tenga onclick
            nombre_maquina = onclick_text.split("'")[1] ### Extraemos el nombre, que para este caso por la estructura de la página analizada, está en la posición 1
            dificultad_maquina = onclick_text.split("'")[3]
            contador += 1

            ### Condiciones para agrupar maquinas por dificultad
            match dificultad_maquina:
                case 'Muy Fácil':
                    lista_muy_facil.append(nombre_maquina)
                case 'Fácil':
                    lista_facil.append(nombre_maquina)
                case 'Medio':
                    lista_medio.append(nombre_maquina)
                case 'Difícil':
                    lista_dificil.append(nombre_maquina)
        
        print(f"{colors.purple} ---> El total de maquinas en {url} es:{colors.end} {contador}\n")    
        maquinas_muy_facil()
        maquinas_facil()
        maquinas_medio()
        maquinas_dificil()

    else: ### Condicional de error
        print(f"ERROR {respuesta.status_code} en la request") ### Mensaje de error

def maquinas_muy_facil():
    print(f"\n{colors.blue} ==========================> Maquinas Muy Fáciles {colors.end}")
    for muyfacil in lista_muy_facil:
        print(f" ==> Maquina: {muyfacil}")

def maquinas_facil():
    print(f"\n{colors.green} ==========================> Maquinas Fáciles {colors.end}")
    for facil in lista_facil:
        print(f" ==> Maquina: {facil}")

def maquinas_medio():
    print(f"\n{colors.orange} ==========================> Maquinas Medias {colors.end}")
    for medio in lista_medio:
        print(f" ==> Maquina: {medio}")

def maquinas_dificil():
    print(f"\n{colors.red} ==========================> Maquinas Difíciles {colors.end}")
    for dificil in lista_dificil:
        print(f" ==> Maquina: {dificil}")

def inicio():
    figlet = Figlet(font='standard')
    ascii_banner = figlet.renderText('SCRAPER')
    print(f"{colors.purple}{ascii_banner}{colors.end}")
    print(f"{colors.purple} ---> SCRAPER – Web Data Extractor developed by Steve{colors.end}")

if __name__ == "__main__":
    main(contador)