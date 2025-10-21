#!/usr/bin/env python3
"""
Upload ESP32 - Script melhorado para upload do projeto
"""

import os
import sys
import subprocess
import time

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_command(cmd, timeout=60):
    """Executa comando e retorna resultado"""
    try:
        print(f"🔄 Executando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            print(f"✅ Sucesso!")
            if result.stdout.strip():
                print(f"📤 Saída: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Erro: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - Comando demorou muito")
        return False
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")
        return False

def check_mpremote():
    """Verifica se mpremote está instalado"""
    try:
        result = subprocess.run(["python", "-m", "mpremote", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ mpremote encontrado: {result.stdout.strip()}")
            return True
        else:
            print("❌ mpremote não encontrado!")
            return False
    except:
        print("❌ mpremote não encontrado!")
        return False

def clear_esp32(port):
    """Limpa arquivos desnecessários do ESP32"""
    print("🧹 Limpando ESP32...")
    
    # Remover pasta .micropico se existir
    run_command(["python", "-m", "mpremote", "connect", port, "exec", 
                "import os; [os.remove(os.path.join('.micropico', f)) for f in os.listdir('.micropico') if os.path.exists('.micropico')]; os.rmdir('.micropico') if os.path.exists('.micropico') and len(os.listdir('.micropico')) == 0 else None"])
    
    # Remover arquivos .pyc se existirem
    run_command(["python", "-m", "mpremote", "connect", port, "exec", 
                "import os; [os.remove(f) for f in os.listdir('.') if f.endswith('.pyc')]"])

def upload_files_selectively(port):
    """Faz upload seletivo dos arquivos"""
    print("📤 Fazendo upload seletivo...")
    
    # Lista de arquivos/pastas essenciais
    essential_files = [
        "main.py",
        "boot.py", 
        "hardware",
        "services",
        "web"
    ]
    
    success_count = 0
    
    for item in essential_files:
        if os.path.exists(item):
            print(f"📁 Enviando: {item}")
            if os.path.isdir(item):
                # É uma pasta
                if run_command(["python", "-m", "mpremote", "connect", port, "fs", "cp", "-r", item, item], timeout=120):
                    success_count += 1
                else:
                    print(f"⚠️ Erro ao enviar pasta {item}")
            else:
                # É um arquivo
                if run_command(["python", "-m", "mpremote", "connect", port, "fs", "cp", item, item], timeout=30):
                    success_count += 1
                else:
                    print(f"⚠️ Erro ao enviar arquivo {item}")
        else:
            print(f"⚠️ {item} não encontrado")
    
    return success_count

def upload_project():
    """Faz upload do projeto para ESP32"""
    print("🚀 Monitor Miner v2.0 - Upload ESP32 Melhorado")
    print("=" * 60)
    
    # Verificar mpremote
    if not check_mpremote():
        print("\n💡 Para instalar mpremote:")
        print("pip install mpremote esptool")
        return False
    
    # Verificar se estamos na pasta correta
    if not os.path.exists("esp32/main.py"):
        print("❌ Arquivo esp32/main.py não encontrado!")
        print("Execute este script na pasta raiz do projeto Monitor Miner")
        return False
    
    print("\n📁 Pasta do projeto: OK")
    print(f"📂 Arquivos Python: {len([f for f in os.listdir('esp32') if f.endswith('.py')])}")
    
    # Mudar para pasta esp32
    os.chdir("esp32")
    
    # Usar porta configurada
    port = ESP32_PORT
    
    print(f"\n🔌 Conectando na porta: {port}")
    
    # Teste de conexão
    print("\n1️⃣ Testando conexão...")
    if not run_command(["python", "-m", "mpremote", "connect", port, "exec", "print('ESP32 OK')"]):
        print(f"❌ Não foi possível conectar na {port}")
        print("💡 Verifique:")
        print("   - ESP32 conectado via USB")
        print("   - Porta COM correta (Device Manager)")
        print("   - Drivers instalados")
        print("   - Fechar outros programas usando a porta")
        return False
    
    # Limpar ESP32
    print("\n2️⃣ Limpando ESP32...")
    clear_esp32(port)
    
    # Upload seletivo
    print("\n3️⃣ Fazendo upload seletivo...")
    success_count = upload_files_selectively(port)
    
    if success_count == 0:
        print("❌ Nenhum arquivo foi enviado!")
        return False
    
    print(f"✅ {success_count} arquivo(s)/pasta(s) enviado(s) com sucesso!")
    
    # Verificar espaço
    print("\n4️⃣ Verificando espaço no ESP32...")
    run_command(["python", "-m", "mpremote", "connect", port, "exec", "import os; print('Espaço livre:', os.statvfs('/')[3] * os.statvfs('/')[0], 'bytes')"])
    
    # Reiniciar ESP32
    print("\n5️⃣ Reiniciando ESP32...")
    if not run_command(["python", "-m", "mpremote", "connect", port, "reset"]):
        print("⚠️ Reinicialização falhou, mas upload pode ter funcionado")
    
    print("\n🎉 UPLOAD CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("\n📋 Próximos passos:")
    print("1. Aguarde 5 segundos para o ESP32 inicializar")
    print("2. Abra monitor serial para ver logs:")
    print(f"   python -m mpremote connect {ESP32_PORT} repl")
    print("3. Procure por: 'AP ativo! SSID: MonitorMiner_Setup'")
    print("4. Conecte no WiFi 'MonitorMiner_Setup' (sem senha)")
    print("5. Acesse: http://192.168.4.1")
    print("6. Configure sua rede WiFi na página")
    print("7. ESP32 reiniciará e conectará automaticamente")
    
    return True

if __name__ == "__main__":
    try:
        success = upload_project()
        if success:
            print("\n✅ Script executado com sucesso!")
        else:
            print("\n❌ Script falhou!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro: {e}")
        sys.exit(1)
