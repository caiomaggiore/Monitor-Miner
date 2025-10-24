#!/bin/bash

echo "============================================================================"
echo "MONITOR MINER v4.0 - UPLOAD PARA ESP32"
echo "============================================================================"
echo

# Verificar se mpremote está instalado
if ! command -v mpremote &> /dev/null; then
    echo "❌ mpremote não encontrado! Instale com: pip install mpremote"
    exit 1
fi

echo "✅ mpremote encontrado"
echo

# Detectar porta COM automaticamente
echo "🔍 Detectando ESP32..."
COM_PORT=$(mpremote connect list | head -n 1)

if [ -z "$COM_PORT" ]; then
    echo "❌ ESP32 não encontrado! Verifique a conexão USB"
    exit 1
fi

echo "✅ ESP32 encontrado na porta: $COM_PORT"
echo

echo "🚀 Iniciando upload da arquitetura v4.0..."
echo

# Upload dos arquivos principais
echo "📁 Uploading arquivos principais..."
mpremote connect $COM_PORT cp esp32/boot.py :
mpremote connect $COM_PORT cp esp32/main.py :
mpremote connect $COM_PORT cp esp32/VERSION.json :

# Upload core modules
echo "📁 Uploading core modules..."
mpremote connect $COM_PORT cp esp32/core/__init__.py :core/
mpremote connect $COM_PORT cp esp32/core/http_server.py :core/
mpremote connect $COM_PORT cp esp32/core/router.py :core/
mpremote connect $COM_PORT cp esp32/core/response.py :core/

# Upload services
echo "📁 Uploading services..."
mpremote connect $COM_PORT cp esp32/services/__init__.py :services/
mpremote connect $COM_PORT cp esp32/services/system_monitor.py :services/
mpremote connect $COM_PORT cp esp32/services/data_store.py :services/

# Upload controllers
echo "📁 Uploading controllers..."
mpremote connect $COM_PORT cp esp32/controllers/__init__.py :controllers/
mpremote connect $COM_PORT cp esp32/controllers/dashboard_controller.py :controllers/
mpremote connect $COM_PORT cp esp32/controllers/config_controller.py :controllers/

# Upload data
echo "📁 Uploading data..."
mpremote connect $COM_PORT cp esp32/data/config.json :data/
mpremote connect $COM_PORT cp esp32/data/sensors_config.json :data/
mpremote connect $COM_PORT cp esp32/data/sensors.json :data/

# Upload web interface
echo "📁 Uploading web interface..."
mpremote connect $COM_PORT cp esp32/web/index.html :web/
mpremote connect $COM_PORT cp esp32/web/config.html :web/

# Upload CSS
echo "📁 Uploading CSS..."
mpremote connect $COM_PORT cp esp32/web/css/base.css :web/css/
mpremote connect $COM_PORT cp esp32/web/css/config.css :web/css/
mpremote connect $COM_PORT cp esp32/web/css/dashboard.css :web/css/
mpremote connect $COM_PORT cp esp32/web/css/nav.css :web/css/
mpremote connect $COM_PORT cp esp32/web/css/style.css :web/css/
mpremote connect $COM_PORT cp esp32/web/css/style.min.css :web/css/

# Upload JavaScript
echo "📁 Uploading JavaScript..."
mpremote connect $COM_PORT cp esp32/web/js/core/components.js :web/js/core/
mpremote connect $COM_PORT cp esp32/web/js/core/dashboard.js :web/js/core/

echo
echo "✅ Upload completo da arquitetura v4.0!"
echo
echo "🌐 Acesse: http://[IP_DO_ESP32]:8080"
echo "📊 Dashboard: http://[IP_DO_ESP32]:8080"
echo "⚙️  Configuração: http://[IP_DO_ESP32]:8080/config"
echo
echo "🎉 Monitor Miner v4.0 - Arquitetura Modular pronta!"
echo
