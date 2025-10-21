#!/usr/bin/env python3
"""
ESP32 Upload - Script simples e confiável
"""

import os
import sys
import subprocess
import time

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_cmd(cmd, timeout=30):
    """Executa comando de forma segura"""
    try:
        print(f"🔄 {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            print(f"✅ OK")
            if result.stdout.strip():
                print(f"📤 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Erro: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Timeout")
        return False
    except Exception as e:
        print(f"💥 {e}")
        return False

def kill_mpremote():
    """Mata todos os processos mpremote"""
    print("🛑 Fechando conexões ativas...")
    run_cmd("taskkill /F /IM python.exe", timeout=5)
    time.sleep(2)

def test_connection():
    """Testa conexão com ESP32"""
    print(f"🔌 Testando conexão {ESP32_PORT}...")
    return run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "print(\\"ESP32 OK\\")"', timeout=10)

def clean_esp32():
    """Limpa arquivos desnecessários"""
    print("🧹 Limpando ESP32...")
    cmd = f'python -m mpremote connect {ESP32_PORT} exec "import os; [os.remove(os.path.join(\\".micropico\\", f)) for f in os.listdir(\\".micropico\\") if os.path.exists(\\".micropico\\")]; os.rmdir(\\".micropico\\") if os.path.exists(\\".micropico\\") and len(os.listdir(\\".micropico\\")) == 0 else None; [os.remove(f) for f in os.listdir(\\".\\") if f.endswith(\\".pyc\\")] if True else None"'
    return run_cmd(cmd, timeout=15)

def upload_file(file_path):
    """Upload um arquivo específico"""
    if os.path.exists(file_path):
        print(f"📁 Enviando: {file_path}")
        if os.path.isdir(file_path):
            cmd = f'python -m mpremote connect {ESP32_PORT} fs cp -r "{file_path}" "{file_path}"'
        else:
            cmd = f'python -m mpremote connect {ESP32_PORT} fs cp "{file_path}" "{file_path}"'
        return run_cmd(cmd, timeout=60)
    else:
        print(f"⚠️ {file_path} não encontrado")
        return False

def main():
    print("🚀 Monitor Miner v2.0 - Upload ESP32")
    print("=" * 50)
    
    # Verificar arquivos essenciais
    if not os.path.exists("esp32/main.py"):
        print("❌ esp32/main.py não encontrado!")
        print("Execute na pasta raiz do projeto Monitor Miner")
        return False
    
    print("📁 Projeto encontrado!")
    
    # Mudar para pasta esp32
    os.chdir("esp32")
    
    # Matar processos ativos
    kill_mpremote()
    
    # Testar conexão
    if not test_connection():
        print("❌ ESP32 não responde!")
        print("💡 Verifique:")
        print("   - ESP32 conectado")
        print(f"   - Porta {ESP32_PORT}")
        print("   - Drivers instalados")
        return False
    
    # Limpar ESP32
    clean_esp32()
    
    # Upload arquivos essenciais
    files_to_upload = ["main.py", "boot.py", "hardware", "services", "web"]
    success_count = 0
    
    print("\n📤 Iniciando upload...")
    for file_path in files_to_upload:
        if upload_file(file_path):
            success_count += 1
    
    if success_count == 0:
        print("❌ Nenhum arquivo enviado!")
        return False
    
    print(f"\n✅ {success_count} arquivo(s) enviado(s)!")
    
    # Verificar espaço
    print("\n📊 Verificando espaço...")
    run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "import os; print(\\"Espaço livre:\\", os.statvfs(\\"/\\")[3] * os.statvfs(\\"/\\")[0], \\"bytes\\")"', timeout=10)
    
    # Reiniciar
    print("\n🔄 Reiniciando ESP32...")
    run_cmd(f'python -m mpremote connect {ESP32_PORT} reset', timeout=10)
    
    print("\n🎉 UPLOAD CONCLUÍDO!")
    print("=" * 50)
    print("\n📋 Próximos passos:")
    print("1. Aguarde 5 segundos")
    print("2. Monitor serial:")
    print(f"   python -m mpremote connect {ESP32_PORT} repl")
    print("3. Procure: 'AP ativo! SSID: MonitorMiner_Setup'")
    print("4. Conecte no WiFi 'MonitorMiner_Setup'")
    print("5. Acesse: http://192.168.4.1")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro: {e}")
        sys.exit(1)
