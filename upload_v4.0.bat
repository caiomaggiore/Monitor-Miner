@echo off
echo ============================================================================
echo MONITOR MINER v4.0 - UPLOAD PARA ESP32
echo ============================================================================
echo.

REM Verificar se mpremote está instalado
where mpremote >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ mpremote não encontrado! Instale com: pip install mpremote
    pause
    exit /b 1
)

echo ✅ mpremote encontrado
echo.

REM Detectar porta COM automaticamente
echo 🔍 Detectando ESP32...
for /f "tokens=*" %%i in ('mpremote connect list') do (
    echo Porta encontrada: %%i
    set COM_PORT=%%i
)

if "%COM_PORT%"=="" (
    echo ❌ ESP32 não encontrado! Verifique a conexão USB
    pause
    exit /b 1
)

echo ✅ ESP32 encontrado na porta: %COM_PORT%
echo.

echo 🚀 Iniciando upload da arquitetura v4.0...
echo.

REM Upload dos arquivos principais
echo 📁 Uploading arquivos principais...
mpremote connect %COM_PORT% cp esp32/boot.py :
mpremote connect %COM_PORT% cp esp32/main.py :
mpremote connect %COM_PORT% cp esp32/VERSION.json :

REM Upload core modules
echo 📁 Uploading core modules...
mpremote connect %COM_PORT% cp esp32/core/__init__.py :core/
mpremote connect %COM_PORT% cp esp32/core/http_server.py :core/
mpremote connect %COM_PORT% cp esp32/core/router.py :core/
mpremote connect %COM_PORT% cp esp32/core/response.py :core/

REM Upload services
echo 📁 Uploading services...
mpremote connect %COM_PORT% cp esp32/services/__init__.py :services/
mpremote connect %COM_PORT% cp esp32/services/system_monitor.py :services/
mpremote connect %COM_PORT% cp esp32/services/data_store.py :services/

REM Upload controllers
echo 📁 Uploading controllers...
mpremote connect %COM_PORT% cp esp32/controllers/__init__.py :controllers/
mpremote connect %COM_PORT% cp esp32/controllers/dashboard_controller.py :controllers/
mpremote connect %COM_PORT% cp esp32/controllers/config_controller.py :controllers/

REM Upload data
echo 📁 Uploading data...
mpremote connect %COM_PORT% cp esp32/data/config.json :data/
mpremote connect %COM_PORT% cp esp32/data/sensors_config.json :data/
mpremote connect %COM_PORT% cp esp32/data/sensors.json :data/

REM Upload web interface
echo 📁 Uploading web interface...
mpremote connect %COM_PORT% cp esp32/web/index.html :web/
mpremote connect %COM_PORT% cp esp32/web/config.html :web/

REM Upload CSS
echo 📁 Uploading CSS...
mpremote connect %COM_PORT% cp esp32/web/css/base.css :web/css/
mpremote connect %COM_PORT% cp esp32/web/css/config.css :web/css/
mpremote connect %COM_PORT% cp esp32/web/css/dashboard.css :web/css/
mpremote connect %COM_PORT% cp esp32/web/css/nav.css :web/css/
mpremote connect %COM_PORT% cp esp32/web/css/style.css :web/css/
mpremote connect %COM_PORT% cp esp32/web/css/style.min.css :web/css/

REM Upload JavaScript
echo 📁 Uploading JavaScript...
mpremote connect %COM_PORT% cp esp32/web/js/core/components.js :web/js/core/
mpremote connect %COM_PORT% cp esp32/web/js/core/dashboard.js :web/js/core/

REM Upload test file
echo 📁 Uploading test file...
mpremote connect %COM_PORT% cp esp32/test_dependencies.py :

echo.
echo ✅ Upload completo da arquitetura v4.0!
echo.
echo 🌐 Acesse: http://[IP_DO_ESP32]:8080
echo 📊 Dashboard: http://[IP_DO_ESP32]:8080
echo ⚙️  Configuração: http://[IP_DO_ESP32]:8080/config
echo.
echo 🎉 Monitor Miner v4.0 - Arquitetura Modular pronta!
echo.
pause
