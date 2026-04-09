@echo off
echo ==========================================
echo       INICIANDO PROYECTO JOBTRACKER
echo ==========================================
echo.
echo Paso 1: Extrayendo datos de Computrabajo...
.\venv\Scripts\python scraper_computrabajo.py
echo.
echo Paso 2: Analizando datos con Inteligencia Artificial...
.\venv\Scripts\python analista_ia.py
echo.
echo ==========================================
echo       PROCESO FINALIZADO CON EXITO
echo ==========================================
pause