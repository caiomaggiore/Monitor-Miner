#!/usr/bin/env python3
"""
Script de Inicialização do ESP32 Manager
Monitor Miner v2.0
"""

import sys
import os

# Verificar se está na pasta correta
if not os.path.exists("tools/esp_manager.py"):
    print("❌ Erro: Execute este script na pasta raiz do projeto Monitor Miner")
    sys.exit(1)

# Importar e executar o manager
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from tools.esp_manager import main
    
    print("🚀 Iniciando ESP32 Manager...")
    print()
    main()
    
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    print()
    print("💡 Instale as dependências:")
    print("   pip install mpremote esptool")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)

