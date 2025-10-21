#!/usr/bin/env python3
"""
Diagnóstico ESP32 - Verifica se MicroPython está instalado corretamente
"""

import subprocess
import sys
import os

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_cmd(cmd, timeout=10):
    """Executa comando e retorna resultado"""
    try:
        print(f"🔄 {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        
        print(f"📤 Return code: {result.returncode}")
        if result.stdout.strip():
            print(f"📤 Saída: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"📤 Erro: {result.stderr.strip()}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"💥 Erro: {e}")
        return False

def check_micropython():
    """Verifica se MicroPython está instalado"""
    print("🐍 Verificando MicroPython...")
    
    # Teste 1: Versão do Python
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import sys; print(sys.version)"'):
        print("❌ MicroPython não responde corretamente")
        return False
    
    # Teste 2: Módulos básicos
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; print(\\"OS module OK\\")"'):
        print("❌ Módulo OS não funciona")
        return False
    
    # Teste 3: Filesystem
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; print(\\"Files:\\", os.listdir(\\".\\"))"'):
        print("❌ Filesystem não funciona")
        return False
    
    print("✅ MicroPython está funcionando!")
    return True

def check_files():
    """Verifica arquivos no ESP32"""
    print("\n📁 Verificando arquivos...")
    
    # Listar arquivos via Python
    if run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; files = os.listdir(\\".\\"); print(\\"Arquivos:\\", files); print(\\"Total:\\", len(files))"'):
        print("✅ Listagem via Python funcionou")
    else:
        print("❌ Erro na listagem via Python")
    
    # Testar se arquivos específicos existem
    files_to_check = ["main.py", "boot.py", "hardware", "services", "web"]
    
    for file in files_to_check:
        cmd = f'python -m mpremote connect {ESP32_PORT} exec "import os; print(\\"{file} existe:\\", os.path.exists(\\"{file}\\"))"'
        run_cmd(cmd)

def check_memory():
    """Verifica memória disponível"""
    print("\n💾 Verificando memória...")
    
    # Espaço livre
    run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; stat = os.statvfs(\\"/\\"); free = stat[3] * stat[0]; print(\\"Espaço livre:\\", free, \\"bytes\\")"')
    
    # Memória RAM
    run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import gc; print(\\"RAM livre:\\", gc.mem_free(), \\"bytes\\")"')

def main():
    print("🔍 Diagnóstico ESP32 - Monitor Miner v2.0")
    print("=" * 50)
    
    # Verificar MicroPython
    if not check_micropython():
        print("\n❌ PROBLEMA: MicroPython não está funcionando corretamente")
        print("💡 Soluções:")
        print("1. Reinstalar MicroPython no ESP32")
        print("2. Verificar se ESP32 não está em modo bootloader")
        print("3. Tentar outro cabo USB")
        return False
    
    # Verificar arquivos
    check_files()
    
    # Verificar memória
    check_memory()
    
    print("\n🎉 DIAGNÓSTICO CONCLUÍDO!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado")
        sys.exit(1)
