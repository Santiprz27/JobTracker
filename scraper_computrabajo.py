import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def main():
    print("\n¡Hola! Vamos a empezar a buscar las mejores ofertas de Computrabajo para ti.")
    
    async with async_playwright() as p:
        navegador = await p.chromium.launch(headless=False)
        pagina = await navegador.new_page()
        
        while True:
            mensaje_pais = """
   Primero, dime en qué país quieres que busque:
   - ar (Argentina)   - mx (México)      - pe (Perú)
   - co (Colombia)    - cl (Chile)       - ec (Ecuador)
   - uy (Uruguay)     - ve (Venezuela)   - cr (Costa Rica)
   Tu respuesta: """
            codpais = input(mensaje_pais).strip().lower()
            if codpais in ["ar", "mx", "pe", "co", "cl", "ec", "uy", "ve", "cr"]:
                break
            print("\nUps, ese código no lo reconozco. ¿Podrías intentar de nuevo?")

        tema = input("\n¿Qué tipo de trabajo te gustaría que analice hoy? (ej: python, css): ").replace(" ", "-").lower()

        while True:
            t_input = input("\n¿Cuántos segundos quieres que espere entre páginas? (Si no sabes, dale Enter y yo me encargo): ").strip()
            if t_input == "":
                wait_time = 2000
                break
            if t_input.replace(",", ".").replace(".", "", 1).isdigit():
                wait_time = int(float(t_input.replace(",", ".")) * 1000)
                break
            print("\nPerdón, necesito que sea un número para saber cuánto esperar.")

        alworks = []
        for npag in range(1, 6):
            url_actual = f"https://{codpais}.computrabajo.com/trabajo-de-{tema}"
            if npag > 1:
                url_actual += f"?p={npag}"
            
            print(f"Buscando ofertas en la página {npag}...")
            await pagina.goto(url_actual)
            await pagina.wait_for_timeout(wait_time)
            
            html = await pagina.content()
            sopa = BeautifulSoup(html, "html.parser")
            ofertas = sopa.find_all("article", class_="box_offer")
            alworks.extend(ofertas)

        print(f"\n¡Genial! Encontré {len(alworks)} posibles empleos para analizar.")

        lista_final = []
        num_a_procesar = 20 
        
        print(f"Ahora voy a entrar a cada uno de los primeros {num_a_procesar} trabajos para leer todo el detalle. Esto puede tardar un poquito...")
        
        for i, tarjeta in enumerate(alworks[:num_a_procesar]):
            link_elem = tarjeta.find("a", class_="js-o-link")
            if not link_elem:
                continue
                
            url_detalle = "https://ar.computrabajo.com" + link_elem['href']
            print(f"[{i+1}/{num_a_procesar}] Leyendo: {url_detalle[:50]}...")
            
            try:
                await pagina.goto(url_detalle)
                await pagina.wait_for_timeout(2000) 
                
                texto_descripcion = await pagina.inner_text('.box_detail')
                
                sopa_det = BeautifulSoup(await pagina.content(), "html.parser")
                titulo = sopa_det.find("h1").text.strip() if sopa_det.find("h1") else "Sin título"
                
                lista_final.append({
                    "Título": titulo,
                    "Link": url_detalle,
                    "Descripción": texto_descripcion
                })
            except Exception:
                print(f"Tuve un problemita al leer este enlace, pero sigo con los demás...")

        if lista_final:
            df = pd.DataFrame(lista_final)
            df.to_csv("ofertas_detalladas.csv", index=False, encoding="utf-8-sig")
            print(f"\n¡Listo! Ya guardé toda la información en 'ofertas_detalladas.csv' para que la IA la analice.")
        
        await navegador.close()

if __name__ == "__main__":
    asyncio.run(main())
