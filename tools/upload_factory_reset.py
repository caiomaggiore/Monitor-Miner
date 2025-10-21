#!/usr/bin/env python3
"""
Upload factory_reset.bin - Reset ESP32 para estado de fábrica
"""

import subprocess
import time
import os
import sys

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_cmd(cmd, timeout=60):
    """Executa comando"""
    try:
        print(f"Executando: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                              timeout=timeout, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            print("OK")
            if result.stdout.strip():
                print(f"Saida: {result.stdout.strip()}")
            return True
        else:
            print(f"Erro: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"Erro: {e}")
        return False

def main():
    print("Upload factory_reset.bin - Reset ESP32")
    print("=" * 40)
    
    # Verificar se arquivo existe
    factory_file = "factory_reset.bin"
    if not os.path.exists(factory_file):
        print(f"Erro: {factory_file} nao encontrado!")
        print("Execute primeiro: python tools/create_factory_reset.py")
        return False
    
    print(f"Arquivo encontrado: {factory_file}")
    size = os.path.getsize(factory_file)
    print(f"Tamanho: {size} bytes")
    
    print("\nATENCAO: Este processo vai RESETAR o ESP32!")
    print("Todos os dados serao perdidos!")
    print("Iniciando em 3 segundos...")
    time.sleep(3)
    
    # Tentar upload via mpremote primeiro (mais suave)
    print("\nTentativa 1: Upload via mpremote...")
    if run_cmd(f'python -m mpremote connect {ESP32_PORT} fs cp "{factory_file}" "{factory_file}"', timeout=30):
        print("factory_reset.bin enviado via mpremote!")
        
        # Tentar executar
        print("\nExecutando factory reset...")
        if run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import machine; machine.reset()"', timeout=15):
            print("Reset executado!")
            time.sleep(5)
            
            # Testar se ESP32 responde
            if run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "print(\'Reset OK\')"', timeout=15):
                print("ESP32 resetado com sucesso!")
                return True
    
    # Tentar upload via esptool (se mpremote falhar)
    print("\nTentativa 2: Upload via esptool...")
    print("IMPORTANTE: ESP32 precisa estar em modo download!")
    print("Faça hard reset: segurar BOOT + pressionar RESET")
    
    if run_cmd(f"python -m esptool --chip esp32 --port {ESP32_PORT} write_flash 0x1000 {factory_file}", timeout=60):
        print("factory_reset.bin enviado via esptool!")
        print("ESP32 deve resetar automaticamente...")
        time.sleep(5)
        
        # Testar se ESP32 responde
        if run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "print(\'Reset OK\')"', timeout=15):
            print("ESP32 resetado com sucesso!")
            return True
    
    print("\nReset falhou!")
    print("Tente:")
    print("1. Hard reset manual (BOOT + RESET)")
    print("2. Executar novamente")
    print("3. python tools/reinstall_micropython.py")
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\nCancelado")
        exit(1)
