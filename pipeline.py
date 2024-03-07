from selenium import webdriver
from datetime import date, timedelta, datetime 
from selenium.webdriver import ActionChains 
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException, ElementNotInteractableException 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 

import pandas as pd
import time
import random
import os
import sys


def set_driver(chrome: bool = True):
    """Initialize the webdriver"""

    print('Iniciando driver.') 

    if chrome:
        print("Iniciando driver, chrome")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    else:
        print("Iniciando driver, Firefox")
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

    print('ok.\n')
    return driver


def r(de:int, a:int) -> int: 
    """genera un randomint(@de, @a)""" 
    return random.randint(de, a)


def duerme(sleep_time:int, stop:int = 0, msg:str = False) -> None: 
    """dormirá durante @sleep_time + un randint(opcional)

    dormirá durante @sleep_time por defecto, si @stop se especifican entonces 
    dormirá un randint(@sleep_time, @stop), en windows imprime cuanto va a dormir,
    y si @msg se especifica se concatena antes de el msg por defecto.
    """
    wait_time = random.randint(sleep_time, stop) if stop else sleep_time

    default_msg = f"{wait_time} sgs..."
    msg = f"{msg}. {default_msg}" if msg else default_msg

    if os.name == "nt":#imprime traza (solo en windows)
        print(msg)

    time.sleep(wait_time)


def click_por_xpath(driver, element:str, xpath:str, bilingual_xpath:str = "", 
                    sleep_time:int = 3, msg:str = ""): 
    """encuentra un elemento del @driver por @xpath, le da click y duerme @sleeptime

    si @msg es dado hace un print con su contenido.

    si el @xpath original no encuentra elemento entonces intentará 
    con @bilingual_xpath, esto para dar soporte a más de un idioma.
    """

    if msg:
        print(msg)

    # 1 intenta dar click
    try:
        driver.find_element(By.XPATH, xpath).click()

    except NoSuchElementException:
        if bilingual_xpath:
            driver.find_element(By.XPATH, bilingual_xpath).click()
        else:
            raise Exception(f"Error, no se pudo localizar el elemento {element}")
        
    except Exception as e:
        print(e)
        driver.close()
        sys.exit(0)

    duerme(sleep_time)


def fill_input(driver, texto:str, element:str, xpath:str, 
               bilingual_xpath:str = "", sleep_time:int = 3, msg:str = ""): 
    """encuentra un input del @driver por @xpath, limpia, escribe y duerme @sleeptime

    si @msg es dado hace un print con su contenido.

    encuentra un input del @driver por @xpath, limpia el contenido 
    y escribe @texto, duerme @sleep_time

    si el @xpath original no encuentra elemento entonces intentará 
    con @bilingual_xpath, esto para dar soporte a más de un idioma.
    """

    if msg:
        print(msg)

    # 1 intenta dar click
    try:
        input_txt = driver.find_element(By.XPATH, xpath)
        input_txt.clear()
        duerme(1)
        input_txt.send_keys(texto)

    except NoSuchElementException:
        if bilingual_xpath:
            input_txt = driver.find_element(By.XPATH, bilingual_xpath)
            input_txt.clear()
            duerme(1)
            input_txt.send_keys(texto)
        else:
            raise Exception(f"Error, no se pudo localizar el elemento {element}")
        
    except Exception as e:
        print(f"Error:{e}")
        driver.close()
        sys.exit(0)

    duerme(sleep_time)


def iniciar_sesion(driver, page_url:str, user:str, password:str):
    """Inicia sesión en la página(@page_url)"""

    driver.get(page_url)
    duerme(5,10)

    click_por_xpath(driver, element="Acceder", xpath='//span[text()="Acceder"]',
                    sleep_time = r(3,6), msg="Iniciando proceso para iniciar sesión")

    fill_input(driver, texto=user, element="Usuario", xpath='//input[@id="wpName1"]', 
               sleep_time=2, msg="Ingresando claves de acceso" )

    fill_input(driver, texto=password, element="contraseña", 
               xpath='//input[@id="wpPassword1"]', sleep_time=2 )

    click_por_xpath(driver, element="Ingresar", xpath='//button[text()="Acceder"]',
                    sleep_time = r(5,9))

    try: 
        driver.find_element(By.XPATH, 
                    '//*[contains(text(), "contraseña que proporcionaste son incorrectos")]'
                ) 
        raise Exception("Error de acceso") 

    except NoSuchElementException: 
        print("Acceso correcto\n")
    
    return driver

 
def extract_table_by_title(driver, page_url:str, title:str, df_header: int = 0, anexos: str = "", 
                           indice_anexos: int = 0, nombre_columna_anexos:str = ""):
    """
    Extrae la primer tabla que encuentre debajo del parrafo que contenga @title en su contenido
    si @anexos no es especificado solo se escribe la tabla tal cual se está en la página.

    Pero si @anexos es especificado, entonces se listarán todas las ligas de los anexos
    de la tabla, para esto ocupamos un @indice_anexos que por xpath buscará todos los 
    elementos del tipo 'a' que estén en la columna  con dicho indice,
    está lista será iterada y por cada liga se visitará dicha página para extrar el 1er
    parrafo cuyo titulo de parrafo contenga @anexos,

    una vez extraído este parrafo se insertará en la tabla original, 
    para esto se crea una columna con el nombre @anexos, y este dato se insertará en la
    fila cuyo valor en @nombre_columna_anexos sea igual al nombre(texto) contenido 
    en la etiqueta 'a'

    ej:
    en la página de méxico la última tabla tiene como @title "Proyecciones de población 
    2010-2030 (CONAPO)", esta tabla tiene sus anexos en la columna 2, llamada "Entidad"
    entonces el @indice_anexos sería 2 y el @nombre_columna_anexos sería "Entidad",
    como en cada liga o anexo lo que se busca es la Toponimia, entonces 
    @anexos sería "Toponimia", el resultado sería que en la tabla original se va a 
    crear una nueva columna llamada toponomía, y por cada anexo que se visité  se escribirá
    el parrafo extraído en dicha columna en la fila dónde correponde el anexo o liga.

    parameters
    ----------
    title: titulo del parrafo del cual queremos extrar su tabla
    df_header: el número de fila que pandas tomará como cabecera
    anexos: nombre de la columna que llevará la info de cada anexo en el excel de salida
    indice_anexos: número de la columna dónde se encuentran las ligas de los anexos
    nombre_columna_de_anexos: nombre de la columna dónde están contenidos las ligas de los anexos

    notas:
    -solo se pueden extraer los anexos de una sola columna
    -solo se puede recuperar la 1er tabla de un "titulo"(@title)
    """
    try:
        xpath = f'//span[contains(text(),"{title}")]/parent::*/following-sibling::table'
        table = driver.find_element(By.XPATH, xpath)
        table_html = table.get_attribute('outerHTML')
    except NoSuchElementException:
        print("Error, no se pudo extraer la tabla solicitada")
        return 

    df = pd.read_html(table_html, header=df_header)[0]

    if anexos:

        #Extrae todos los links de la tabla(solo los de una columna dada por @indice_anexos)
        xpath = f'./tbody/tr/td[{indice_anexos}]/descendant::a[contains(@href,"wiki")]'
        links_de_anexos = table.find_elements(By.XPATH, xpath)

        #crea una nueva "columna"
        df[anexos] = 'Sin link'

        for link_anexo in links_de_anexos:
            """
            Itera una lista de anexos y extrae un parrafo de cada uno
            
            Itera una lista de anexos(links), lo visita,
            busca un dato especifico y extrae el 1er parrafo
            si no encuentra el dato buscado agrega 'Sin dato'
            """
            try:
                nombre_del_dato = link_anexo.text

                print(f"visitando: {nombre_del_dato}")
                driver.execute_script("arguments[0].scrollIntoView(true);", link_anexo)
                duerme(1,2)

                #Encuentra el elemento en la columna de la izquierda
                columna_izq = link_anexo.find_element(By.XPATH,'./ancestor::td/preceding-sibling::td') 
                ActionChains(driver).move_to_element(columna_izq).pause(2).perform()

                ActionChains(driver).click(link_anexo).perform()
                duerme(4,8)

                print("extrayendo parrafo")
                try:
                    xpath = f'//span[contains(text(),"{anexos}")]/parent::*/following-sibling::p'
                    parrafo = driver.find_element(By.XPATH, xpath).text
                except NoSuchElementException: 
                    print(f"No se encontró {anexos}.")    
                    parrafo = 'Sin dato'

                try:
                    df[anexos][df[nombre_columna_anexos] == nombre_del_dato] = parrafo
                except Exception as e:
                    print(f"No se pudo anexar el dato\n{e}")
                
                print("Volviendo a página principal")
                driver.back()
                duerme(4,8)

            except Exception as e:
                print("Algo salió mal en este anexo.")
                driver.back(page_url)
                duerme(4,8)
    
    file_name = title.replace(" ", "_") + ".xlsx"
    df.to_excel(file_name, sheet_name='ai27', index=False, encoding='utf-8')
    print(f"Archivo {file_name} creado con exito.\n")


def main():
    """
    Extrae las tablas de una página de wikipedia
    dada una url (mex_url) lo primero que hace es iniciar 
    sesión(user, password), ya en la página cargada llama
    al metodo extract_table_by_title() por cada tabla que se 
    quiera extraer, la función busca un elemento que contenga
    un texto(titulo_primer_tabla) y a partir de ese elemento 
    encuentra la 1er tabla 'hija' la cuál es convertida
    con pandas en un archivo .xlsx, adicional a esto dicha
    función puede visitar todos los links o anexos de una sola 
    de sus columnas pero para todas sus filas, recupera cierto 
    parrafo y lo guarda en una columna nueva de la tabla extraída.
    """    
    #URl's a extraer
    usa_url = "https://es.wikipedia.org/wiki/Estado_de_los_Estados_Unidos"
    mex_url = "https://es.wikipedia.org/w/index.php?title=Anexo:Entidades_federativas_de_M%C3%A9xico_por_superficie,_poblaci%C3%B3n_y_densidad"
    
    # Credenciales de la cuenta ya creada para iniciar sesión en wikipedia
    user = "cristobalgarzalazar"
    password = "pruebaai27"

    #titulos de los parrafos "padre" de cada tabla
    titulo_primer_tabla = "Entidades federativas de México por superficie, población y densidad"
    titulo_segunda_tabla = "Censos (INEGI) 1900-2020"
    titulo_tercer_tabla = "Proyecciones de población 2010-2030 (CONAPO)"
    titulo_primer_tabla_usa = "Estados"

    #define si se extrae el flujo para México o para USA
    mexico = True


    driver = set_driver()

    if mexico: 
        driver = iniciar_sesion(driver=driver, page_url=mex_url, user=user, password=password)
        
        #2
        extract_table_by_title(driver, page_url=mex_url, title=titulo_primer_tabla, df_header=1)
        extract_table_by_title(driver, page_url=mex_url, title=titulo_segunda_tabla, df_header=1)
        extract_table_by_title(driver, page_url=mex_url, title=titulo_tercer_tabla, df_header=1,
                               anexos="Toponimia", indice_anexos=2, 
                               nombre_columna_anexos='Entidad')
    
    else: #USA
        driver = iniciar_sesion(driver=driver, page_url=usa_url, user=user, password=password)

        #2
        extract_table_by_title(driver, page_url=usa_url, title=titulo_primer_tabla_usa, 
                               anexos="Etimología", indice_anexos=2, nombre_columna_anexos='Estado')
    
    driver.quit()
    print("Tarea finalizada OK")
    #*1 Estas variables hay que meterlas en un archivo de configración
    #*2 Este proceso debe ser iterativo dado un archivo de configuración
    #   recorrer todas las urls y cada tabla correpondiente a esa url,
    #   así como cada anexo(link) 
        

if __name__ == "__main__":
    main()