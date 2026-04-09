# scraper_computrabajo.py
# Aquí escribiremos nuestro scraper desde cero.
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd


async def main():
    print("Iniciando nuestro scraper de Computrabajo...")
    
    async with async_playwright() as p:
        # 1. Lanzamos el navegador de Chrome/Chromium 
        # (headless=False significa "No lo ocultes, quiero verlo funcionar")
        navegador = await p.chromium.launch(headless=False)
        
        # 2. Abrimos una pestaña nueva
        pagina = await navegador.new_page()
        
        # 3. Vamos a la página y buscamos empleos de Python
        flag = True
        while(flag):
            mensaje_pais = """
            Ingrese el código de su país para buscar en Computrabajo:
            - ar (Argentina)   - mx (México)      - pe (Perú)
            - co (Colombia)    - cl (Chile)       - ec (Ecuador)
            - uy (Uruguay)     - ve (Venezuela)   - cr (Costa Rica)
            Código: """
            codpais = input(mensaje_pais).strip().lower() # .strip es eliminar caracteres en blanco, .lower es convertir a minusculas
            tema = input("Ingrese el tema a buscar: ").replace(" ", "-").replace(",", "-").lower()
            url = f"https://{codpais}.computrabajo.com/trabajo-de-{tema}"
            url2=f"https://{codpais}.computrabajo.com/trabajo-de-{tema}?p=2"
            url3=f"https://{codpais}.computrabajo.com/trabajo-de-{tema}?p=3"
            
            if codpais not in ["ar", "mx", "pe", "co", "cl", "ec", "uy", "ve", "cr"]:
                print("Código de país no válido. Por favor, intente nuevamente.")
                flag = True

            else:
                time = input("Ingrese el tiempo en segundos que desea que espere entre cada página: ") 
                if time == "":
                    wait_time = 2000
                    break

                if time.isdigit(): # Verifica si el texto son solo números
                    wait_time = int(time) * 1000 # Convertimos a número y pasamos a milisegundos
                    break
                else:
                    print("Error: Por favor, ingrese un número entero válido.")

 

        alworks = []

        for npag in range (1,6):
                if npag ==1:
                    url_actual = f"https://{codpais}.computrabajo.com/trabajo-de-{tema}"
                    print(f"\nNavegando a: {url_actual}")
                else:
                    url_actual = f"https://{codpais}.computrabajo.com/trabajo-de-{tema}?p={npag}"
                    print(f"\nNavegando a: {url_actual} página {npag}")
                await pagina.goto(url_actual)
                await pagina.wait_for_timeout(wait_time)
                html_pagina = await pagina.content() #Playwright hace un "Copy/Paste" del código HTML (el pagina.content()).
                sopa_pagina = BeautifulSoup(html_pagina, "html.parser")
                           # Esto es lo que "llena la bolsa" en cada vuelta del bucle
                trabajos_de_esta_pagina = sopa_pagina.find_all("article", class_="box_offer")
                alworks.extend(trabajos_de_esta_pagina) # alworks es una bolsa de articulos asi es mas facil es analisis




        
        tarjetas_de_empleo = sopa_pagina.find_all("article", class_="box_offer")
        print(f"\nSe encontraron {len(tarjetas_de_empleo)} ofertas de empleo en la pantalla.")
        
        # 7. Recorremos las primeras 5 ofertas para imprimir su título
 # Creamos una lista para los datos limpios
        lista_final = []
        
        # 1. Primero sacamos los links de todos los trabajos que juntamos
        print(f"\nExtrayendo links de {len(alworks)} ofertas...")
        enlaces_y_datos = []
        for tarjeta in alworks:
            link_elem = tarjeta.find("a", class_="js-o-link")
            if link_elem:
                url_trabajo = "https://ar.computrabajo.com" + link_elem['href']
                enlaces_y_datos.append(url_trabajo)

        # 2. SEGUNDO PASO: Visitar los primeros 3 para traer la Super Descripción
        # (Cambiamos el 3 por len(enlaces_y_datos) si quieres traer TODOS)
        print("\n--- Iniciando Deep Scraping (Extrayendo descripciones largas) ---")
        for i, link in enumerate(enlaces_y_datos[:20]):
            print(f"[{i+1}/20] Visitando detalle: {link}")
            
            await pagina.goto(link)
            await pagina.wait_for_timeout(1) # Esperamos a que cargue el detalle
            
            html_detalle = await pagina.content()
            sopa_detalle = BeautifulSoup(html_detalle, "html.parser")
            
            # Buscamos la descripción que tú encontraste
            desc_larga = sopa_detalle.find("div", class_="fs16 t_word_wrap")
            texto_descripcion = desc_larga.text.strip() if desc_larga else "No se pudo leer la descripción larga"
            
            # Buscamos el título y empresa en esta nueva pantalla
            titulo = sopa_detalle.find("h1").text.strip() if sopa_detalle.find("h1") else "Sin título"
            
            lista_final.append({
                "Título": titulo,
                "Link": link,
                "Descripción Completa": texto_descripcion
            })

        # 3. Guardamos el resultado pro
        if lista_final:
            df = pd.DataFrame(lista_final)
            df.to_csv("ofertas_detalladas.csv", index=False, encoding="utf-8-sig")
            print(f"\n¡LISTO! Se creó 'ofertas_detalladas.csv' con las descripciones reales.")

if __name__ == "__main__":
    # Función asincrónica
    asyncio.run(main())
