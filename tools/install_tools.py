#!/usr/bin/env python3
"""
Instalar Ferramentas Necessárias - esptool e mpremote
"""

import subprocess
import sys
import os

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_pip_install(package):
    """Instala pacote via pip"""
    try:
        print(f"📦 Instalando {package}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"✅ {package} instalado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao instalar {package}")
            print(f"Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"💥 Erro: {e}")
        return False

def check_tool(tool_name, test_cmd):
    """Verifica se ferramenta está instalada"""
    try:
        result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ {tool_name} já está instalado!")
            return True
        else:
            print(f"❌ {tool_name} não encontrado")
            return False
    except Exception as e:
        print(f"❌ {tool_name} não encontrado: {e}")
        return False

def main():
    print("🔧 Instalador de Ferramentas ESP32")
    print("=" * 40)
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Verificar pip
    if not check_tool("pip", "python -m pip --version"):
        print("❌ pip não encontrado!")
        return False
    
    # Lista de ferramentas necessárias
    tools = [
        ("esptool", "python -m esptool --help"),
        ("mpremote", "python -m mpremote --help"),
        ("pyserial", "python -c 'import serial; print(\"OK\")'")
    ]
    
    # Verificar quais já estão instaladas
    installed = []
    missing = []
    
    for tool, test_cmd in tools:
        if check_tool(tool, test_cmd):
            installed.append(tool)
        else:
            missing.append(tool)
    
    print(f"\n📊 Status:")
    print(f"✅ Instaladas: {', '.join(installed) if installed else 'Nenhuma'}")
    print(f"❌ Faltando: {', '.join(missing) if missing else 'Nenhuma'}")
    
    # Instalar ferramentas faltantes
    if missing:
        print(f"\n🔧 Instalando ferramentas faltantes...")
        
        success_count = 0
        for tool in missing:
            if run_pip_install(tool):
                success_count += 1
        
        print(f"\n📊 Resultado: {success_count}/{len(missing)} ferramentas instaladas")
        
        if success_count == len(missing):
            print("🎉 Todas as ferramentas instaladas!")
        else:
            print("⚠️ Algumas ferramentas falharam na instalação")
    else:
        print("\n🎉 Todas as ferramentas já estão instaladas!")
    
    # Verificação final
    print(f"\n🧪 Verificação final...")
    all_ok = True
    
    for tool, test_cmd in tools:
        if not check_tool(tool, test_cmd):
            all_ok = False
    
    if all_ok:
        print("\n🎉 SUCESSO! Todas as ferramentas estão funcionando!")
        print("\n📋 Próximos passos:")
        print("1. python tools/download_firmware_smart.py")
        print("2. python tools/format_esp32_auto.py")
        print("3. python simple_upload.py")
        return True
    else:
        print("\n❌ Algumas ferramentas ainda não funcionam")
        print("💡 Tente:")
        print("1. Reiniciar o terminal")
        print("2. Executar PowerShell como Administrador")
        print("3. Reinstalar Python")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado pelo usuário")
        exit(1)
