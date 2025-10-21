#!/usr/bin/env python3
"""
Hard Reset ESP32 - Força modo download para esptool
"""

import subprocess
import time
import os
import sys

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_cmd(cmd, timeout=30):
    """Executa comando"""
    try:
        print(f"🔄 {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                              timeout=timeout, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            print("✅ OK")
            if result.stdout.strip():
                print(f"📤 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Erro: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"💥 {e}")
        return False

def main():
    print("🔧 Hard Reset ESP32 - Forçar Modo Download")
    print("=" * 50)
    
    print("📋 INSTRUÇÕES IMPORTANTES:")
    print("1. 🛑 DESCONECTE o cabo USB do ESP32")
    print("2. ⏳ Aguarde 5 segundos")
    print("3. 🔌 RECONECTE o cabo USB")
    print("4. ⚡ Pressione e SEGURE o botão BOOT do ESP32")
    print("5. ⚡ Pressione o botão RESET (mantendo BOOT pressionado)")
    print("6. 🔄 Solte RESET, depois solte BOOT")
    print("7. ✅ ESP32 estará em modo download")
    
    print("\n⚠️ ATENÇÃO:")
    print("- Botão BOOT = GPIO0 (geralmente ao lado do botão RESET)")
    print("- Botão RESET = botão de reinicialização")
    print("- Faça isso com o cabo USB conectado!")
    
    print("\n🚀 Quando estiver pronto, pressione Enter...")
    input()
    
    # Testar se ESP32 está em modo download
    print("\n🔍 Testando modo download...")
    
    # Tentar conectar com esptool
    if run_cmd(f"python -m esptool --chip esp32 --port {ESP32_PORT} chip_id", timeout=10):
        print("✅ ESP32 em modo download!")
        print("\n📋 Próximos passos:")
        print("1. python tools/reinstall_micropython.py")
        print("2. python simple_upload.py")
        return True
    else:
        print("❌ ESP32 ainda não está em modo download")
        print("\n💡 Tente novamente:")
        print("1. Desconectar USB")
        print("2. Aguardar 5 segundos")
        print("3. Reconectar USB")
        print("4. Segurar BOOT + pressionar RESET")
        print("5. Soltar RESET, depois BOOT")
        print("6. Executar novamente este script")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n🔄 Execute novamente após fazer o hard reset")
            exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado")
        exit(1)
