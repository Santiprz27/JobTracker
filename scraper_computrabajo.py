import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def main():
    print("🚀 Iniciando JobTracker: Scraper de Computrabajo...")
    
    async with async_playwright() as p:
        # 1. Configuración del Navegador
        navegador = await p.chromium.launch(headless=False)
        pagina = await navegador.new_page()
        
        # 2. Entrada de Datos y Validación
        while True:
            mensaje_pais = """
    Ingrese el código de su país:
    - ar (Argentina)   - mx (México)      - pe (Perú)
    - co (Colombia)    - cl (Chile)       - ec (Ecuador)
    - uy (Uruguay)     - ve (Venezuela)   - cr (Costa Rica)
    Código: """
            codpais = input(mensaje_pais).strip().lower()
            if codpais in ["ar", "mx", "pe", "co", "cl", "ec", "uy", "ve", "cr"]:
                break
            print("Error: Código de país no válido.")

        tema = input("¿Qué puesto buscamos? (ej: python): ").replace(" ", "-").lower()

        while True:
            t_input = input("Segundos de espera entre páginas (Enter para 2s): ").strip()
            if t_input == "":
                wait_time = 2000
                break
            if t_input.replace(",", ".").replace(".", "", 1).isdigit():
                wait_time = int(float(t_input.replace(",", ".")) * 1000)
                break
            print("Error: Ingrese un número válido.")

        # 3. Recolección de Listado (Páginas 1 a 5)
        alworks = []
        for npag in range(1, 6):
            url_actual = f"https://{codpais}.computrabajo.com/trabajo-de-{tema}"
            if npag > 1:
                url_actual += f"?p={npag}"
            
            print(f"Navegando a página {npag}...")
            await pagina.goto(url_actual)
            await pagina.wait_for_timeout(wait_time)
            
            html = await pagina.content()
            sopa = BeautifulSoup(html, "html.parser")
            ofertas = sopa.find_all("article", class_="box_offer")
            alworks.extend(ofertas)

        print(f"Se encontraron {len(alworks)} ofertas en el listado.")

        # 4. Deep Scraping (Extracción de detalles reales)
        lista_final = []
        num_a_procesar = 20 # Puedes subirlo a len(alworks) si deseas procesar todo
        
        print(f"\nIniciando Deep Scraping ({num_a_procesar} ofertas)...")
        
        for i, tarjeta in enumerate(alworks[:num_a_procesar]):
            link_elem = tarjeta.find("a", class_="js-o-link")
            if not link_elem:
                continue
                
            url_detalle = "https://ar.computrabajo.com" + link_elem['href']
            print(f"[{i+1}/{num_a_procesar}] Procesando: {url_detalle[:60]}...")
            
            try:
                await pagina.goto(url_detalle)
                await pagina.wait_for_timeout(2000) # Tiempo para carga de JS
                
                # Extraemos todo el texto visible del detalle
                texto_descripcion = await pagina.inner_text('.box_detail')
                
                sopa_det = BeautifulSoup(await pagina.content(), "html.parser")
                titulo = sopa_det.find("h1").text.strip() if sopa_det.find("h1") else "Sin título"
                
                lista_final.append({
                    "Título": titulo,
                    "Link": url_detalle,
                    "Descripción": texto_descripcion
                })
            except Exception as e:
                print(f"Error en {url_detalle}: {e}")

        # 5. Guardado de Datos
        if lista_final:
            df = pd.DataFrame(lista_final)
            df.to_csv("ofertas_detalladas.csv", index=False, encoding="utf-8-sig")
            print(f"\nArchivo 'ofertas_detalladas.csv' guardado con éxito.")
        
        await navegador.close()

if __name__ == "__main__":
    asyncio.run(main())
