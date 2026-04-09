<h1 align="center">
  <br>
  JobTracker
  <br>
</h1>

<h4 align="center">Scraper de Empleos y Analista con IA.</h4>

<p align="center">
  <em>Leer en otros idiomas: <a href="README.md">Inglés</a>, <a href="README-es.md">Español</a></em>
</p>

<p align="center">
  <a href="#-características">Características</a> •
  <a href="#-cómo-funciona">Cómo Funciona</a> •
  <a href="#-instalación-y-uso">Instalación y Uso</a> •
  <a href="#-arquitectura">Arquitectura</a> •
  <a href="#-tecnologías">Tecnologías</a>
</p>

---

**JobTracker** es una potente herramienta de automatización diseñada para extraer, procesar y analizar ofertas de empleo de Computrabajo a escala. Combinando web scraping de alta velocidad con las capacidades analíticas de **Llama 3.3 (vía Groq API)**, transforma descripciones básicas en información estratégica del mercado.

Ofrece un flujo de trabajo fluido desde la recolección automatizada hasta resúmenes profesionales generados por IA.

## ✨ Características

- 🕷️ **Lógica de Scraping Profundo**: A diferencia de los scrapers básicos, JobTracker visita cada link individual para extraer descripciones completas, salarios y requisitos específicos.
- 🤖 **Inteligencia Artificial**: Integrado con **Groq (Llama-3.3-70b)** para identificar habilidades técnicas top, niveles de experiencia y consejos estratégicos.
- ⚡ **Núcleo Asincrónico**: Construido con **Playwright**, permitiendo una navegación rápida y confiable por múltiples páginas y contenido dinámico.
- 🔑 **Seguridad Portable**: Gestión de archivos `.env` para mantener las API Keys privadas, con un sistema automático de solicitud de clave para nuevos usuarios.
- 🎨 **Estética CLI**: Interfaz de terminal con arte ASCII personalizado y soporte para UTF-8.
- 📂 **Exportación Estructurada**: Genera archivos CSV detallados (`utf-8-sig`) listos para usar en Excel o Google Sheets.

---

## 🚀 Cómo Funciona

JobTracker sigue un proceso de ejecución de dos fases para asegurar la calidad de los datos y la inteligencia del análisis.

### 1. Motor de Extracción (Deep Scraping)
El scraper utiliza **Playwright** para recorrer las páginas de resultados. Por cada oferta, realiza una segunda navegación al detalle. En lugar de selectores frágiles, usa una extracción robusta de `inner_text` sobre el contenedor `.box_detail`, capturando el 100% de la información visible aunque el diseño de la web cambie ligeramente.

### 2. Procesador Analítico (Groq / Llama 3.3)
El módulo analítico consume el CSV generado. Para evitar el desbordamiento de tokens manteniendo la precisión, implementa un truncado inteligente (toma los primeros 15 puestos con 1000 caracteres por descripción). Envía este contexto de alto valor a **Llama 3.3**, que extrae patrones que a un humano le tomaría horas identificar.

---

## 💻 Instalación y Uso

### Prerrequisitos
- Python 3.10 o superior.
- Una **API Key de Groq** gratuita (se obtiene en [console.groq.com](https://console.groq.com)).

### Pasos
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Santiprz27/JobTracker.git
   cd JobTracker
   ```
2. **Configurar el entorno virtual**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
4. **Ejecutar la aplicación**:
   Doble clic en `ejecutar.bat` o corre:
   ```bash
   .\venv\Scripts\python scraper_computrabajo.py
   ```

---

## 🏗️ Arquitectura

```text
JobTracker/
├── scraper_computrabajo.py      # Motor de scraping (Playwright + BS4).
├── analista_ia.py               # Módulo analítico (Groq API + Pandas).
├── ejecutar.bat                 # Orquestador con arte ASCII.
├── .env                         # Variables de entorno (API Keys).
├── .gitignore                   # Reglas de seguridad para Git.
└── ofertas_detalladas.csv       # Base de datos local de empleos.
```

---

## ⚙️ Tecnologías

- **[Playwright](https://playwright.dev/python/)** automatización web de alto rendimiento.
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** para procesar HTML.
- **[Groq SDK](https://console.groq.com/)** para inferencia ultra-rápida con Llama 3.3.
- **[Pandas](https://pandas.pydata.org/)** para gestión de datos y CSV.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** para manejo seguro de claves.

---
> Proyecto desarrollado con enfoque en automatización web y análisis de mercado con LLMs.
