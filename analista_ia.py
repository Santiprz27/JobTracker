import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

def analizar_mercado():
    print("Cargando...")
    
    # 1. Carga de configuración
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: No se encontró GROQ_API_KEY en el archivo .env")
        return

    client = Groq(api_key=api_key)

    # 2. Carga de Datos
    try:
        df = pd.read_csv("ofertas_detalladas.csv")
    except FileNotFoundError:
        print("Error: No se encontró 'ofertas_detalladas.csv'.")
        return

    # 3. Preparación de Datos (Truncamos para no exceder límites de tokens)
    texto_jobs = ""
    for _, fila in df.head(15).iterrows():
        # Tomamos solo los primeros 1000 caracteres de cada descripción
        desc_limpia = str(fila['Descripción'])[:1000]
        texto_jobs += f"\nPUESTO: {fila['Título']}\n📝 DETALLE: {desc_limpia}\n"

    # 4. Consulta a la IA
    prompt = f"""
    Eres un experto en el mercado laboral tecnológico. Analiza esta lista de empleos:
    {texto_jobs}
    
    Por favor, responde de forma concisa:
    1. Top 3-5 habilidades técnicas más demandadas.
    2. Nivel de experiencia dominante.
    3. Breve consejo estratégico para candidatos.
    4. sueldo si es mencionado
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        
        # 5. Visualización de Resultados
        print("\n" + "═"*50)
        print("RESUMEN ESTRATÉGICO DE MERCADO")
        print("═"*50)
        print(completion.choices[0].message.content)
        print("═"*50)

    except Exception as e:
        print(f"Error al consultar Groq: {e}")

if __name__ == "__main__":
    analizar_mercado()