#!/usr/bin/env python3
"""
Teste Simples ESP32 - Verifica se está funcionando
"""

import subprocess
import sys
import os

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_cmd(cmd, timeout=10):
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

def main():
    print("🧪 Teste Simples ESP32")
    print("=" * 30)
    
    # Teste 1: Conectar
    print("\n🔌 Teste 1: Conectar ao ESP32...")
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "print(\'ESP32 OK\')"'):
        print("❌ ESP32 não responde!")
        print("💡 Possíveis causas:")
        print("   - ESP32 não conectado")
        print(f"   - Porta {ESP32_PORT} incorreta")
        print("   - Drivers não instalados")
        print("   - ESP32 em modo bootloader")
        return False
    
    # Teste 2: MicroPython
    print("\n🐍 Teste 2: MicroPython...")
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import sys; print(\'Python:\', sys.version)"'):
        print("❌ MicroPython com problema!")
        return False
    
    # Teste 3: Filesystem
    print("\n📁 Teste 3: Filesystem...")
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; print(\'Files:\', os.listdir(\'.\'))"'):
        print("❌ Filesystem com problema!")
        return False
    
    # Teste 4: Espaço
    print("\n💾 Teste 4: Espaço disponível...")
    if not run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; stat = os.statvfs(\'/\'); print(\'Espaço livre:\', stat[3] * stat[0], \'bytes\')"'):
        print("❌ Erro ao verificar espaço!")
        return False
    
    print("\n🎉 TODOS OS TESTES PASSARAM!")
    print("✅ ESP32 está funcionando perfeitamente!")
    
    print("\n📋 Próximos passos:")
    print("1. python simple_upload.py")
    print("2. python diagnose_esp32.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado pelo usuário")
        exit(1)
