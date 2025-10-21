#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload File by File - Envia arquivos individualmente para ESP32
Solucao para filesystem corrompido que nao aceita pastas
"""

import os
import subprocess
import sys
import time

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
from port_config import ESP32_PORT

def run_cmd(cmd, timeout=30):
    """Executa comando"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                              timeout=timeout, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def upload_single_file(local_path, remote_path):
    """Upload um arquivo individual"""
    cmd = f'python -m mpremote connect {ESP32_PORT} fs cp "{local_path}" "{remote_path}"'
    success, msg = run_cmd(cmd)
    
    if success:
        print(f"OK: {remote_path}")
        return True
    else:
        print(f"ERRO: {remote_path} - {msg}")
        return False

def create_dir_if_needed(dir_path):
    """Tenta criar diretorio no ESP32"""
    cmd = f'python -m mpremote connect {ESP32_PORT} exec "import os; os.mkdir(\'{dir_path}\')"'
    success, msg = run_cmd(cmd)
    
    if success or "OSError" in msg:
        return True
    return False

def get_all_python_files():
    """Lista todos os arquivos Python do projeto"""
    files = []
    
    # Arquivos na raiz
    for f in ["main.py", "boot.py"]:
        if os.path.exists(f):
            files.append((f, f))
    
    # Arquivos em hardware/
    if os.path.exists("hardware"):
        for f in os.listdir("hardware"):
            if f.endswith(".py"):
                files.append((f"hardware/{f}", f"hardware/{f}"))
    
    # Arquivos em services/
    if os.path.exists("services"):
        for f in os.listdir("services"):
            if f.endswith(".py"):
                files.append((f"services/{f}", f"services/{f}"))
    
    # Arquivos web (HTML, CSS, JS)
    for root, dirs, filenames in os.walk("web"):
        for f in filenames:
            local = os.path.join(root, f)
            remote = local.replace("\\", "/")
            files.append((local, remote))
    
    return files

def main():
    print("=" * 50)
    print("Upload File by File - ESP32")
    print("=" * 50)
    
    # Verificar se esp32/ existe
    if not os.path.exists("esp32/main.py"):
        print("ERRO: esp32/main.py nao encontrado!")
        print("Execute na pasta raiz do projeto")
        return False
    
    # Mudar para pasta esp32
    os.chdir("esp32")
    
    # Matar processos Python ativos
    print("\nLiberando porta...")
    run_cmd("taskkill /F /IM python.exe", timeout=5)
    time.sleep(2)
    
    # Testar conexao
    print("Testando conexao...")
    success, msg = run_cmd(f'python -m mpremote connect {ESP32_PORT} exec "print(\'OK\')"')
    if not success:
        print(f"ERRO: ESP32 nao responde - {msg}")
        return False
    print("ESP32 conectado!")
    
    # Criar diretorios
    print("\nCriando diretorios...")
    dirs_to_create = ["hardware", "services", "web", "web/css", "web/js", "web/js/components"]
    for d in dirs_to_create:
        create_dir_if_needed(d)
    
    # Listar arquivos para upload
    files = get_all_python_files()
    print(f"\nTotal de arquivos: {len(files)}")
    
    # Upload arquivo por arquivo
    print("\nIniciando upload...")
    success_count = 0
    failed_count = 0
    
    for i, (local, remote) in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {remote}... ", end="")
        if upload_single_file(local, remote):
            success_count += 1
        else:
            failed_count += 1
    
    # Resultado
    print("\n" + "=" * 50)
    print(f"Sucesso: {success_count}")
    print(f"Falhas: {failed_count}")
    print("=" * 50)
    
    if success_count > 0:
        # Reiniciar ESP32
        print("\nReiniciando ESP32...")
        run_cmd(f'python -m mpremote connect {ESP32_PORT} reset')
        
        print("\nUPLOAD CONCLUIDO!")
        print("\nProximos passos:")
        print("1. Aguarde 5 segundos")
        print(f"2. python -m mpremote connect {ESP32_PORT} repl")
        print("3. Ver logs e IP do ESP32")
        return True
    else:
        print("\nNenhum arquivo enviado!")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelado")
        sys.exit(1)

