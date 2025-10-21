#!/usr/bin/env python3
"""
Configuração centralizada da porta ESP32
Lê a porta do arquivo config.py ou usa padrão
"""

import os
import sys

# Adicionar pasta pai ao path para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_esp32_port():
    """
    Retorna a porta COM do ESP32 configurada
    
    Prioridade:
    1. Arquivo config.py (ESP32_PORT)
    2. Variável de ambiente ESP32_PORT
    3. Padrão: COM5 (Windows) ou /dev/ttyUSB0 (Linux/Mac)
    """
    try:
        # Tentar importar do config.py
        import config
        if hasattr(config, 'ESP32_PORT'):
            port = config.ESP32_PORT
            print(f"📌 Usando porta do config.py: {port}")
            return port
    except ImportError:
        # config.py não existe, usar padrão
        pass
    except Exception as e:
        print(f"⚠️ Erro ao ler config.py: {e}")
    
    # Tentar variável de ambiente
    env_port = os.environ.get('ESP32_PORT')
    if env_port:
        print(f"📌 Usando porta da variável de ambiente: {env_port}")
        return env_port
    
    # Usar padrão baseado no sistema operacional
    default_port = "COM5" if sys.platform == "win32" else "/dev/ttyUSB0"
    print(f"📌 Usando porta padrão: {default_port}")
    print(f"💡 Dica: Crie um arquivo config.py com ESP32_PORT='SuaPorta' para configurar")
    
    return default_port

def get_esp32_baudrate():
    """
    Retorna o baudrate do ESP32 configurado
    """
    try:
        import config
        if hasattr(config, 'ESP32_BAUDRATE'):
            return config.ESP32_BAUDRATE
    except:
        pass
    
    return 115200  # Padrão

# Para importação fácil
ESP32_PORT = get_esp32_port()
ESP32_BAUDRATE = get_esp32_baudrate()

if __name__ == "__main__":
    print("🔌 Configuração ESP32")
    print("=" * 40)
    print(f"Porta: {ESP32_PORT}")
    print(f"Baudrate: {ESP32_BAUDRATE}")

