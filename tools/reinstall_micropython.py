#!/usr/bin/env python3
"""
Reinstalar MicroPython - Script simples sem problemas de encoding
"""

import subprocess
import time
import os
import sys

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_simple(cmd, timeout=60):
    """Executa comando de forma simples"""
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

def find_firmware():
    """Procura firmware MicroPython"""
    locations = [
        "esp32-micropython.bin",
        "firmware/esp32-micropython.bin"
    ]
    
    for location in locations:
        if os.path.exists(location):
            print(f"📦 Firmware encontrado: {location}")
            return location
    
    print("❌ Firmware não encontrado!")
    print("💡 Execute: python tools/download_firmware_smart.py")
    return None

def main():
    print("🔧 Reinstalar MicroPython - Script Simples")
    print("=" * 50)
    
    # Verificar se esptool está instalado
    print("🔍 Verificando esptool...")
    if not run_simple("python -c \"import esptool; print('esptool OK')\""):
        print("❌ esptool não encontrado!")
        print("💡 Execute: python tools/install_tools.py")
        return False
    
    # Procurar firmware
    firmware = find_firmware()
    if not firmware:
        return False
    
    print("⚠️ ATENÇÃO: Vai APAGAR TUDO no ESP32!")
    print("🚀 Iniciando em 3 segundos...")
    time.sleep(3)
    
    # Apagar flash
    print("🧹 Apagando flash...")
    if not run_simple(f"python -m esptool --chip esp32 --port {ESP32_PORT} erase_flash", timeout=60):
        print("❌ Erro ao apagar flash")
        return False
    
    # Aguardar
    time.sleep(3)
    
    # Gravar firmware
    print("📝 Gravando MicroPython...")
    cmd = f"python -m esptool --chip esp32 --port {ESP32_PORT} write_flash -z 0x1000 {firmware}"
    if not run_simple(cmd, timeout=120):
        print("❌ Erro ao gravar firmware")
        return False
    
    print("✅ MicroPython reinstalado!")
    
    # Testar
    print("\n🧪 Testando...")
    time.sleep(5)
    
    if run_simple(f'python -m mpremote connect {ESP32_PORT} exec "print(\'OK\')"', timeout=20):
        print("✅ ESP32 funcionando!")
        
        # Verificar espaço
        if run_simple(f'python -m mpremote connect {ESP32_PORT} exec "import os; stat = os.statvfs(\'/\'); print(\'Espaço:\', stat[3] * stat[0])"', timeout=20):
            print("\n🎉 REINSTALAÇÃO CONCLUÍDA!")
            print("\n📋 Próximos passos:")
            print("1. python simple_upload.py")
            print("2. python diagnose_esp32.py")
            return True
    
    print("❌ Reinstalação falhou!")
    return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado")
        exit(1)
