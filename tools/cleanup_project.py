#!/usr/bin/env python3
"""
Limpeza do Projeto - Remove arquivos desnecessários e organiza estrutura
"""

import os
import shutil
import sys

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def move_to_tools(filename, description):
    """Move arquivo para pasta tools"""
    if os.path.exists(filename):
        try:
            shutil.move(filename, f"tools/{filename}")
            print(f"✅ {description} movido para tools/")
            return True
        except Exception as e:
            print(f"❌ Erro ao mover {filename}: {e}")
            return False
    return False

def remove_file(filename, description):
    """Remove arquivo desnecessário"""
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"🗑️ {description} removido")
            return True
        except Exception as e:
            print(f"❌ Erro ao remover {filename}: {e}")
            return False
    return False

def remove_duplicate_folder(folder_path, description):
    """Remove pasta duplicada"""
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"🗑️ {description} removida")
            return True
        except Exception as e:
            print(f"❌ Erro ao remover {folder_path}: {e}")
            return False
    return False

def main():
    print("🧹 Limpeza do Projeto Monitor Miner")
    print("=" * 40)
    
    # Arquivos para mover para tools/
    files_to_move = [
        ("diagnose_esp32.py", "Diagnóstico ESP32"),
        ("download_firmware.py", "Download firmware (antigo)"),
        ("esp32_upload.py", "Upload ESP32 (antigo)"),
        ("format_esp32.py", "Formatar ESP32 (antigo)"),
        ("install_micropython.py", "Instalar MicroPython (antigo)"),
        ("simple_upload.py", "Upload simples"),
        ("test_esp32.py", "Teste ESP32 (antigo)"),
        ("upload_esp32.py", "Upload ESP32 (alternativo)")
    ]
    
    # Arquivos para remover
    files_to_remove = [
        ("ESP32_GENERIC-20250911-v1.26.1.bin", "Firmware duplicado na raiz"),
        ("esp32-micropython.bin", "Firmware duplicado na raiz"),
        ("file", "Arquivo estranho"),
        ("requirements.txt", "Requirements (não necessário para ESP32)")
    ]
    
    # Pastas duplicadas para remover
    folders_to_remove = [
        ("hardware/hardware", "Pasta hardware duplicada"),
        ("services/services", "Pasta services duplicada"),
        ("web/web", "Pasta web duplicada"),
        ("api", "Pasta api vazia")
    ]
    
    print("\n📁 Movendo scripts para tools/...")
    moved_count = 0
    for filename, description in files_to_move:
        if move_to_tools(filename, description):
            moved_count += 1
    
    print(f"\n✅ {moved_count} arquivo(s) movido(s) para tools/")
    
    print("\n🗑️ Removendo arquivos desnecessários...")
    removed_count = 0
    for filename, description in files_to_remove:
        if remove_file(filename, description):
            removed_count += 1
    
    print(f"\n✅ {removed_count} arquivo(s) removido(s)")
    
    print("\n🗑️ Removendo pastas duplicadas...")
    folders_removed = 0
    for folder_path, description in folders_to_remove:
        if remove_duplicate_folder(folder_path, description):
            folders_removed += 1
    
    print(f"\n✅ {folders_removed} pasta(s) removida(s)")
    
    # Verificar estrutura final
    print("\n📊 Estrutura final:")
    important_files = [
        "main.py",
        "boot.py", 
        "config.example.py",
        "pymakr.conf",
        "README.md"
    ]
    
    important_folders = [
        "hardware",
        "services", 
        "web",
        "tools",
        "firmware",
        "data"
    ]
    
    print("\n📄 Arquivos principais na raiz:")
    for file in important_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (faltando)")
    
    print("\n📁 Pastas principais:")
    for folder in important_folders:
        if os.path.exists(folder):
            print(f"✅ {folder}/")
        else:
            print(f"❌ {folder}/ (faltando)")
    
    print("\n🎉 LIMPEZA CONCLUÍDA!")
    print("\n📋 Estrutura organizada:")
    print("📄 Raiz: Apenas arquivos essenciais")
    print("📁 tools/: Scripts de gerenciamento")
    print("📁 firmware/: Firmwares baixados")
    print("📁 hardware/, services/, web/: Código do projeto")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado pelo usuário")
        exit(1)
