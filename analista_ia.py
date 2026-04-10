import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

def analizar_mercado():
    print("\n¡Ahora vamos con la parte inteligente! Estoy despertando al analista...")
    
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("\nOye, parece que no encontré tu llave de Groq.")
        api_key = input("¿Podrías pegarla aquí para que pueda trabajar?: ").strip()
        with open(".env", "a") as f:
            f.write(f"\nGROQ_API_KEY={api_key}")
        print("¡Genial! Ya la guardé para que no tengas que ponerla la próxima vez.")

    client = Groq(api_key=api_key)

    try:
        df = pd.read_csv("ofertas_detalladas.csv")
    except FileNotFoundError:
        print("\nUy, parece que todavía no tienes el archivo de ofertas. Primero corre el recolector de datos.")
        return

    texto_jobs = ""
    for _, fila in df.head(15).iterrows():
        desc_limpia = str(fila['Descripción'])[:1000]
        texto_jobs += f"\n📌 PUESTO: {fila['Título']}\n📝 DETALLE: {desc_limpia}\n"

    prompt = f"""
    Eres un experto en el mercado laboral tecnológico. Analiza esta lista de empleos:
    {texto_jobs}
    
    Por favor, responde de forma amigable y concisa:
    1. ¿Cuáles son las 3-5 habilidades técnicas más pedidas?
    2. ¿Qué nivel de experiencia están buscando generalmente?
    3. Un consejo estratégico para quienes quieran aplicar.
    4. ¿Se menciona algo sobre el sueldo?
    """

    print("Le estoy preguntando a la IA qué opina sobre estos trabajos. Dame unos segundos...")
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        
        print("\n" + "═"*50)
        print("              LO QUE DESCUBRÍ PARA TI")
        print("═"*50)
        print(completion.choices[0].message.content)
        print("═"*50)
        print("\n¡Espero que esta información te sirva para conseguir ese puesto!")

    except Exception:
        print("\nTuve un pequeño problema al hablar con la IA. Revisa tu conexión o tu API Key.")

if __name__ == "__main__":
    analizar_mercado()