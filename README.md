<h1 align="center">
  <br>
  JobTracker
  <br>
</h1>

<h4 align="center">AI-Powered Job Market Scraper & Analyst.</h4>

<p align="center">
  <em>Read this in other languages: <a href="README.md">English</a>, <a href="README-es.md">Español</a></em>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-how-it-works">How It Works</a> •
  <a href="#-installation-and-usage">Installation & Usage</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a>
</p>

---

**JobTracker** is a powerful automation tool designed to extract, process, and analyze job postings from Computrabajo at scale. By combining high-speed web scraping with the analytical capabilities of **Llama 3.3 (via Groq API)**, it transforms raw job descriptions into actionable market insights.

It provides a seamless workflow from automated data collection to professional strategic summaries.

## ✨ Features

- 🕷️ **Deep Scraper Logic**: Unlike basic scrapers, JobTracker visits each individual job link to extract full descriptions, salary info, and specific requirements.
- 🤖 **AI Intelligence**: Integrated with **Groq (Llama-3.3-70b)** to identify top technical skills, experience levels, and strategic advice for candidates.
- ⚡ **Asynchronous Core**: Built on **Playwright**, allowing for fast and reliable navigation through dozens of pages and dynamic content.
- 🔑 **Portable Security**: Uses encrypted `.env` management to keep API keys safe and private, with an automated fallback to manual input for new users.
- 🎨 **CLI Aesthetics**: Features a custom ASCII-art terminal interface with UTF-8 support for a premium developer experience.
- 📂 **Structured Data Export**: Automatically generates detailed CSV files (`utf-8-sig`) for further analysis or spreadsheet management.

---

## 🚀 How It Works

JobTracker follows a dual-phase execution pipeline to ensure data quality and intelligence.

### 1. Extraction Engine (Deep Scraping)
The scraper uses **Playwright** to navigate multiple result pages. For each job found, it performs a second-pass navigation to the detail URL. Instead of relying on fragile CSS selectors, it employs a robust `inner_text` extraction of the `.box_detail` container, capturing 100% of the visible information (requirements, benefits, full text) even if the platform layout changes slightly.

### 2. Analytical Processor (Groq / Llama 3.3)
The analytical module consumes the generated CSV. To prevent token overflow while maintaining the highest precision, it implements a smart truncation algorithm. It sends this condensed high-value context to **Llama 3.3**, which extracts patterns that a human would take hours to identify.

---

## 💻 Installation and Usage

### Prerequisites
- Python 3.10 or higher.
- A free **Groq API Key** (obtainable at [console.groq.com](https://console.groq.com)).

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Santiprz27/JobTracker.git
   cd JobTracker
   ```
2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
4. **Run the application**:
   Double click on `ejecutar.bat` or run:
   ```bash
   .\venv\Scripts\python scraper_computrabajo.py
   ```

---

## 🏗️ Architecture

```text
JobTracker/
├── scraper_computrabajo.py      # Main scraping engine (Playwright + BS4).
├── analista_ia.py               # AI Analytics module (Groq API + Pandas).
├── ejecutar.bat                 # Automated CLI orchestrator with custom ASCII art.
├── .env                         # Local environment variables (API Keys).
├── .gitignore                   # Safety rules to exclude sensitive data and venv.
└── ofertas_detalladas.csv       # Flattened database of extracted jobs.
```

---

## ⚙️ Tech Stack

- **[Playwright](https://playwright.dev/python/)** for high-performance web automation.
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** for HTML parsing and data structure cleanup.
- **[Groq SDK](https://console.groq.com/)** for lightning-fast inference using Llama 3.3.
- **[Pandas](https://pandas.pydata.org/)** for data management and CSV processing.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** for secure variable handling.

---
> Project developed with a focus on web automation and LLM market analysis.
