#!/usr/bin/env python3
"""
Upload Simples ESP32 - Apenas o essencial
"""

import os
import subprocess
import sys

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_simple(cmd):
    """Executa comando de forma simples"""
    try:
        print(f"🔄 {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ OK")
            return True
        else:
            print(f"❌ Erro: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"💥 {e}")
        return False

def upload_file(filename):
    """Upload um arquivo específico"""
    if os.path.exists(filename):
        print(f"📁 Enviando: {filename}")
        cmd = f'python -m mpremote connect {ESP32_PORT} fs cp "{filename}" "{filename}"'
        return run_simple(cmd)
    else:
        print(f"⚠️ {filename} não encontrado")
        return False

def main():
    print("🚀 Upload Simples ESP32")
    print("=" * 30)
    
    # Verificar arquivos
    if not os.path.exists("esp32/main.py"):
        print("❌ esp32/main.py não encontrado!")
        print("Execute na pasta raiz do projeto")
        return False
    
    # Mudar para pasta esp32
    os.chdir("esp32")
    
    # Upload arquivos essenciais um por um
    files_to_upload = ["main.py", "boot.py", "hardware", "services", "web"]
    success_count = 0
    
    print("\n📤 Iniciando upload...")
    for file_path in files_to_upload:
        if upload_file(file_path):
            success_count += 1
    
    if success_count > 0:
        print(f"\n✅ {success_count} arquivo(s) enviado(s)!")
        
        # Reiniciar
        print("\n🔄 Reiniciando ESP32...")
        run_simple(f'python -m mpremote connect {ESP32_PORT} reset')
        
        print("\n🎉 UPLOAD CONCLUÍDO!")
        print("\n📋 Próximos passos:")
        print("1. Aguarde 5 segundos")
        print(f"2. Monitor: python -m mpremote connect {ESP32_PORT} repl")
        print("3. Procure: 'MonitorMiner_Setup'")
        return True
    else:
        print("\n❌ Nenhum arquivo enviado!")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado")
        sys.exit(1)