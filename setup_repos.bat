@echo off
echo ========================================
echo Configurando Repositorios Git
echo ========================================
echo.

echo [1/4] Monitor Miner - ESP32
cd esp32
git add .
git commit -m "feat: versao inicial estavel - WiFi AP + Servidor Web + Hello World"
echo.
echo Status:
git status
cd ..

echo.
echo [2/4] IDE ESP Cursor - Ferramentas CLI
cd IDE-ESP-Cursor
git add .
git commit -m "feat: IDE ESP32 - ferramentas CLI completas para desenvolvimento"
echo.
echo Status:
git status
cd ..

echo.
echo ========================================
echo Pronto para Push!
echo ========================================
echo.
echo Para fazer push:
echo   cd esp32
echo   git push -u origin main
echo.
echo   cd ../IDE-ESP-Cursor
echo   git push -u origin main
echo.

pause

