@echo off
echo ================================================================
echo  Navegacion Urbana - Grupo E
echo  Iniciando backend + frontend
echo ================================================================
echo.

echo [1/3] Instalando dependencias Python...
pip install -r backend\requirements.txt

echo.
echo [2/3] Iniciando backend FastAPI en http://localhost:8000 ...
start "Backend API" cmd /c "python backend\main.py"

echo Esperando 5 segundos a que el backend cargue el grafo...
ping -n 5 127.0.0.1 > nul

echo.
echo [3/3] Iniciando frontend Nuxt en http://localhost:3000 ...
cd frontend
start "Frontend Nuxt" cmd /c "npm run dev"

echo.
echo ================================================================
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:3000
echo ================================================================
echo  Abre http://localhost:3000 en tu navegador.
echo  Haz clic en el mapa para marcar ORIGEN y DESTINO.
echo ================================================================
pause
