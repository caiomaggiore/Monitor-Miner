#!/usr/bin/env python3
"""
Formatar ESP32 Forçado - Método 2 (Reinstalação Completa)
"""

import subprocess
import time
import os
import glob
import sys

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_cmd(cmd, timeout=60):
    """Executa comando com encoding correto"""
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
    patterns = [
        "../esp32-micropython.bin",
        "../firmware/esp32-micropython.bin",
        "esp32-micropython.bin",
        "esp32-*.bin",
        "*.bin"
    ]
    
    for pattern in patterns:
        files = glob.glob(pattern)
        if files:
            print(f"📦 Firmware encontrado: {files[0]}")
            return files[0]
    
    print("❌ Firmware não encontrado!")
    print("💡 Execute: python tools/download_firmware_smart.py")
    return None

def erase_and_reinstall():
    """Apaga flash e reinstala MicroPython - MÉTODO 2 FORÇADO"""
    print("🧹 MÉTODO 2: Reinstalação Completa do MicroPython")
    print("=" * 50)
    
    # Verificar esptool (comando simples)
    print("🔍 Verificando esptool...")
    if not run_cmd("python -c \"import esptool; print('esptool OK')\""):
        print("❌ esptool não encontrado!")
        print("💡 Execute: python tools/install_tools.py")
        return False
    
    # Procurar firmware
    firmware = find_firmware()
    if not firmware:
        return False
    
    # Apagar flash (usar python -m esptool)
    print("🧹 Apagando flash completo...")
    if not run_cmd(f"python -m esptool --chip esp32 --port {ESP32_PORT} erase_flash", timeout=60):
        print("❌ Erro ao apagar flash")
        return False
    
    # Aguardar
    print("⏳ Aguardando 3 segundos...")
    time.sleep(3)
    
    # Gravar firmware (usar python -m esptool)
    print("📝 Gravando MicroPython...")
    cmd = f"python -m esptool --chip esp32 --port {ESP32_PORT} write_flash -z 0x1000 {firmware}"
    if not run_cmd(cmd, timeout=120):
        print("❌ Erro ao gravar firmware")
        return False
    
    print("✅ MicroPython reinstalado!")
    return True

def test_after_format():
    """Testa se está funcionando"""
    print("\n🧪 Testando após reinstalação...")
    time.sleep(5)  # Aguardar mais tempo para inicialização
    
    # Teste básico
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "print(\'Teste OK\')"', timeout=20):
        print("❌ ESP32 não responde")
        return False
    
    # Teste filesystem
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; print(\'Files:\', os.listdir(\'.\'))"', timeout=20):
        print("❌ Filesystem com problema")
        return False
    
    # Teste espaço
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; stat = os.statvfs(\'/\'); print(\'Espaço livre:\', stat[3] * stat[0], \'bytes\')"', timeout=20):
        print("❌ Erro no espaço")
        return False
    
    print("✅ ESP32 funcionando perfeitamente!")
    return True

def main():
    print("🔧 Formatador ESP32 Forçado - Método 2")
    print("=" * 50)
    
    print("⚠️ ATENÇÃO: Vai APAGAR TUDO no ESP32!")
    print("🚀 Iniciando reinstalação completa em 3 segundos...")
    time.sleep(3)
    
    # Método 2: Reinstalar MicroPython
    print("\n📋 MÉTODO 2: Reinstalar MicroPython...")
    if erase_and_reinstall():
        if test_after_format():
            print("\n🎉 ESP32 FORMATADO E FUNCIONANDO!")
            print("\n📋 Próximos passos:")
            print("1. python simple_upload.py")
            print("2. python diagnose_esp32.py")
            return True
    
    print("\n❌ Formatação falhou!")
    print("💡 Tente:")
    print("1. Baixar firmware: python tools/download_firmware_smart.py")
    print("2. Instalar ferramentas: python tools/install_tools.py")
    print("3. Executar novamente")
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado")
        exit(1)
