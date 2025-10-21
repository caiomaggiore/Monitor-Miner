#!/usr/bin/env python3
"""
Download Inteligente de Firmware MicroPython - Detecta versão mais recente
"""

import urllib.request
import os
import re
import sys

# Adicionar pasta pai ao path para importar outros módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def download_firmware_smart():
    """Baixa firmware MicroPython mais recente automaticamente"""
    print("📥 Download Inteligente de Firmware MicroPython")
    print("=" * 50)
    
    # Criar pasta firmware se não existir
    firmware_dir = "../firmware"
    if not os.path.exists(firmware_dir):
        os.makedirs(firmware_dir)
        print(f"📁 Criada pasta: {firmware_dir}")
    
    # URLs oficiais para tentar (em ordem de preferência) - PADRÃO CORRETO
    urls = [
        # Versão mais recente (v1.26.1 - 2025-09-11) - PADRÃO CORRETO
        "https://micropython.org/resources/firmware/ESP32_GENERIC-20250911-v1.26.1.bin",
        # Versão estável anterior (v1.25.0 - 2025-04-15)
        "https://micropython.org/resources/firmware/ESP32_GENERIC-20250415-v1.25.0.bin",
        # Versão estável (v1.24.1 - 2024-11-29)
        "https://micropython.org/resources/firmware/ESP32_GENERIC-20241129-v1.24.1.bin",
        # Versão que estava funcionando (v1.23.0 - 2024-06-02)
        "https://micropython.org/resources/firmware/ESP32_GENERIC-20240602-v1.23.0.bin",
        # Versão estável mais antiga (v1.21.0 - 2023-10-05)
        "https://micropython.org/resources/firmware/ESP32_GENERIC-20231005-v1.21.0.bin"
    ]
    
    # Salvar na pasta firmware
    filename = os.path.join(firmware_dir, "esp32-micropython.bin")
    filename_root = "../esp32-micropython.bin"  # Também na raiz para compatibilidade
    
    print("🔍 Tentando baixar firmware mais recente...")
    
    for i, url in enumerate(urls, 1):
        try:
            print(f"\n📋 Tentativa {i}/{len(urls)}")
            
            # Extrair versão da URL
            version_match = re.search(r'v(\d+\.\d+\.\d+)', url)
            version = version_match.group(1) if version_match else "desconhecida"
            
            print(f"🌐 URL: {url}")
            print(f"📦 Versão: {version}")
            
            # Baixar arquivo com timeout e headers
            print("⬇️ Baixando...")
            
            # Usar urllib com headers para evitar bloqueios
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(filename, 'wb') as f:
                    f.write(response.read())
            
            # Copiar também para a raiz (compatibilidade)
            if os.path.exists(filename):
                import shutil
                shutil.copy2(filename, filename_root)
            
            # Verificar se baixou
            if os.path.exists(filename) and os.path.exists(filename_root):
                size = os.path.getsize(filename)
                print(f"✅ Sucesso! Firmware baixado!")
                print(f"📁 Arquivo: {filename}")
                print(f"📁 Cópia: {filename_root}")
                print(f"📏 Tamanho: {size:,} bytes")
                print(f"🔖 Versão: {version}")
                return True
            else:
                print("❌ Arquivo não foi criado")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue
    
    print("\n❌ Todas as tentativas falharam!")
    print("💡 Soluções:")
    print("1. Verifique sua conexão com a internet")
    print("2. Baixe manualmente de: https://micropython.org/download/ESP32_GENERIC/")
    print("3. Salve como: esp32-micropython.bin")
    print("4. Tente executar PowerShell como Administrador")
    
    return False

def verify_firmware():
    """Verifica se o firmware baixado é válido"""
    filename = "../esp32-micropython.bin"
    
    if not os.path.exists(filename):
        print("❌ Firmware não encontrado!")
        return False
    
    size = os.path.getsize(filename)
    
    print(f"\n🔍 Verificando firmware...")
    print(f"📁 Arquivo: {filename}")
    print(f"📏 Tamanho: {size:,} bytes")
    
    # Tamanho típico de firmware ESP32 MicroPython
    if size < 1_000_000:  # Menos de 1MB
        print("⚠️ Arquivo muito pequeno - pode estar corrompido")
        return False
    elif size > 10_000_000:  # Mais de 10MB
        print("⚠️ Arquivo muito grande - pode não ser firmware")
        return False
    else:
        print("✅ Arquivo parece válido!")
        return True

def main():
    print("🚀 Download Inteligente de Firmware ESP32")
    print("=" * 50)
    
    # Verificar se já existe
    if os.path.exists("../esp32-micropython.bin"):
        print("📁 Firmware já existe!")
        if verify_firmware():
            print("✅ Firmware válido encontrado!")
            print("\n📋 Próximos passos:")
            print("1. python tools/format_esp32_auto.py")
            print("2. python simple_upload.py")
            return True
        else:
            print("❌ Firmware inválido - baixando novo...")
            os.remove("../esp32-micropython.bin")
    
    # Baixar firmware
    if download_firmware_smart():
        if verify_firmware():
            print("\n🎉 FIRMWARE BAIXADO COM SUCESSO!")
            print("\n📋 Próximos passos:")
            print("1. python tools/format_esp32_auto.py")
            print("2. python simple_upload.py")
            print("3. python diagnose_esp32.py")
            return True
    
    print("\n❌ FALHA NO DOWNLOAD")
    return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Cancelado pelo usuário")
        exit(1)
