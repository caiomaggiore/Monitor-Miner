#!/usr/bin/env python3
"""
Auto Hard Reset ESP32 - Tenta forçar modo download automaticamente
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

def try_boot_mode():
    """Tenta forçar ESP32 para modo boot"""
    print("🔧 Tentando forçar modo boot...")
    
    # Método 1: Reset via mpremote
    print("\n📋 Método 1: Reset via mpremote...")
    if run_cmd(f'python -m mpremote connect {ESP32_PORT} reset', timeout=10):
        time.sleep(2)
        if run_cmd(f"python -m esptool --chip esp32 --port {ESP32_PORT} chip_id", timeout=10):
            print("✅ Modo boot ativado!")
            return True
    
    # Método 2: Tentar com diferentes parâmetros
    print("\n📋 Método 2: Tentar com parâmetros diferentes...")
    if run_cmd(f"python -m esptool --chip esp32 --port {ESP32_PORT} --baud 115200 chip_id", timeout=10):
        print("✅ Modo boot ativado!")
        return True
    
    # Método 3: Tentar sem especificar chip
    print("\n📋 Método 3: Tentar sem especificar chip...")
    if run_cmd(f"python -m esptool --port {ESP32_PORT} chip_id", timeout=10):
        print("✅ Modo boot ativado!")
        return True
    
    return False

def main():
    print("🔧 Auto Hard Reset ESP32")
    print("=" * 30)
    
    # Verificar se ESP32 responde normalmente
    print("🔍 Verificando ESP32...")
    if run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "print(\'OK\')"', timeout=10):
        print("✅ ESP32 funcionando (modo normal)")
    else:
        print("❌ ESP32 não responde")
        return False
    
    # Tentar forçar modo boot
    if try_boot_mode():
        print("\n🎉 ESP32 EM MODO BOOT!")
        print("\n📋 Próximos passos:")
        print("1. python tools/reinstall_micropython.py")
        print("2. python simple_upload.py")
        return True
    else:
        print("\n❌ Não foi possível forçar modo boot automaticamente")
        print("\n💡 SOLUÇÃO MANUAL:")
        print("1. 🛑 Desconectar cabo USB")
        print("2. ⏳ Aguardar 5 segundos")
        print("3. 🔌 Reconectar cabo USB")
        print("4. ⚡ SEGURAR botão BOOT")
        print("5. ⚡ Pressionar botão RESET (mantendo BOOT)")
        print("6. 🔄 Soltar RESET, depois BOOT")
        print("7. ✅ Executar: python tools/reinstall_micropython.py")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n🔄 Execute o hard reset manual e tente novamente")
            exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado")
        exit(1)
