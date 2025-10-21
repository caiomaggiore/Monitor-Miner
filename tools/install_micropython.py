#!/usr/bin/env python3
"""
Instalar MicroPython no ESP32
"""

import subprocess
import os
import sys

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_cmd(cmd, timeout=60):
    """Executa comando"""
    try:
        print(f"🔄 {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        
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

def download_firmware():
    """Baixa firmware MicroPython"""
    print("📥 Baixando firmware MicroPython...")
    
    # URL do firmware mais recente
    url = "https://micropython.org/resources/firmware/esp32-20231005-v1.21.0.bin"
    filename = "esp32-micropython.bin"
    
    print(f"💡 Baixe manualmente de: {url}")
    print(f"💡 Salve como: {filename}")
    print("💡 Coloque na pasta do projeto")
    
    return filename

def install_firmware(filename):
    """Instala firmware no ESP32"""
    print(f"🔧 Instalando firmware: {filename}")
    
    if not os.path.exists(filename):
        print(f"❌ Arquivo {filename} não encontrado!")
        print("💡 Baixe o firmware primeiro")
        return False
    
    # Apagar flash
    print("🧹 Apagando flash...")
    if not run_cmd(f"esptool --chip esp32 --port {ESP32_PORT} erase_flash", timeout=60):
        print("❌ Erro ao apagar flash")
        return False
    
    # Gravar firmware
    print("📝 Gravando MicroPython...")
    cmd = f"esptool --chip esp32 --port {ESP32_PORT} write_flash -z 0x1000 {filename}"
    if not run_cmd(cmd, timeout=120):
        print("❌ Erro ao gravar firmware")
        return False
    
    print("✅ MicroPython instalado!")
    return True

def install_microdot():
    """Instala Microdot via mip"""
    print("📦 Instalando Microdot...")
    
    # Aguardar ESP32 inicializar
    import time
    time.sleep(3)
    
    # Instalar via mip
    if run_cmd(f"python -m mpremote connect {ESP32_PORT} mip install microdot", timeout=120):
        print("✅ Microdot instalado!")
        return True
    else:
        print("❌ Erro ao instalar Microdot")
        return False

def main():
    print("🔧 Instalador MicroPython ESP32")
    print("=" * 40)
    
    print("⚠️ ATENÇÃO: Este processo vai APAGAR tudo no ESP32!")
    
    # Verificar se esptool está instalado
    if not run_cmd("esptool --version"):
        print("❌ esptool não encontrado!")
        print("💡 Instale com: pip install esptool")
        return False
    
    # Baixar firmware
    filename = download_firmware()
    
    print(f"\n📁 Coloque o arquivo {filename} na pasta do projeto")
    input("Pressione Enter quando tiver o arquivo...")
    
    # Instalar firmware
    if not install_firmware(filename):
        return False
    
    # Instalar Microdot
    if not install_microdot():
        print("⚠️ Microdot não instalado, mas MicroPython está OK")
    
    print("\n🎉 INSTALAÇÃO CONCLUÍDA!")
    print("📋 Próximos passos:")
    print("1. python diagnose_esp32.py")
    print("2. python simple_upload.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado")
        sys.exit(1)
