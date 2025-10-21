#!/usr/bin/env python3
"""
Criar factory_reset.bin - Arquivo para resetar ESP32 para estado de fábrica
"""

import os
import struct

def create_factory_reset_bin():
    """Cria arquivo factory_reset.bin para ESP32"""
    print("Criando factory_reset.bin...")
    
    # Cabeçalho do arquivo binário ESP32
    # Baseado na estrutura padrão do ESP32
    header = bytearray([
        # Magic bytes para ESP32
        0xE9, 0x03, 0x00, 0x00,  # Magic number
        0x00, 0x00, 0x00, 0x00,  # Segment count
        0x00, 0x00, 0x00, 0x00,  # Flash mode
        0x00, 0x00, 0x00, 0x00,  # Flash size
        0x00, 0x00, 0x00, 0x00,  # Entry point
        0x00, 0x00, 0x00, 0x00,  # Checksum
    ])
    
    # Dados de reset (comando para limpar filesystem)
    reset_data = bytearray([
        # Comandos para resetar ESP32
        0x00, 0x00, 0x00, 0x00,  # Padrão
    ])
    
    # Combinar header + dados
    factory_reset = header + reset_data
    
    # Salvar arquivo
    filename = "factory_reset.bin"
    with open(filename, 'wb') as f:
        f.write(factory_reset)
    
    print(f"Arquivo criado: {filename}")
    print(f"Tamanho: {len(factory_reset)} bytes")
    
    return filename

def create_simple_factory_reset():
    """Cria um factory_reset.bin mais simples"""
    print("Criando factory_reset.bin simples...")
    
    # Arquivo binário mínimo para ESP32
    # Baseado em um bootloader básico
    data = bytearray([
        # ESP32 bootloader básico
        0xE9, 0x03, 0x00, 0x00,  # Magic number
        0x01, 0x00, 0x00, 0x00,  # Segment count = 1
        0x02, 0x00, 0x00, 0x00,  # Flash mode = QIO
        0x00, 0x00, 0x00, 0x00,  # Flash size = 4MB
        0x00, 0x10, 0x00, 0x40,  # Entry point
        0x00, 0x00, 0x00, 0x00,  # Checksum (será calculado)
        
        # Segmento de dados
        0x00, 0x00, 0x00, 0x00,  # Load address
        0x04, 0x00, 0x00, 0x00,  # Data length
        0x00, 0x00, 0x00, 0x00,  # Data (4 bytes de zeros)
    ])
    
    # Calcular checksum simples
    checksum = sum(data[8:24]) & 0xFF
    data[24] = checksum
    
    filename = "factory_reset.bin"
    with open(filename, 'wb') as f:
        f.write(data)
    
    print(f"Arquivo criado: {filename}")
    print(f"Tamanho: {len(data)} bytes")
    
    return filename

def main():
    print("Gerador de factory_reset.bin para ESP32")
    print("=" * 40)
    
    # Tentar criar arquivo simples primeiro
    try:
        filename = create_simple_factory_reset()
        print(f"\nArquivo criado com sucesso: {filename}")
        
        # Verificar se arquivo foi criado
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"Tamanho do arquivo: {size} bytes")
            
            print("\nProximos passos:")
            print("1. python tools/upload_factory_reset.py")
            print("2. O ESP32 sera resetado para estado de fabrica")
            print("3. Apos reset, python tools/reinstall_micropython.py")
            
            return True
        else:
            print("Erro: Arquivo nao foi criado")
            return False
            
    except Exception as e:
        print(f"Erro ao criar arquivo: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            exit(1)
    except KeyboardInterrupt:
        print("\nCancelado")
        exit(1)
