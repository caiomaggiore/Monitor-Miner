#!/usr/bin/env python3
"""
Monitor Miner - Script de Validação de Release
Valida que a versão está pronta para ser commitada e testada

Versão: 1.0.0
Data: 17/10/2025
"""

import json
import os
import sys
from pathlib import Path

# Cores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text:^60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}[OK] {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}[ERRO] {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}[AVISO] {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}[INFO] {text}{Colors.END}")

def check_file_exists(filepath, description):
    """Verifica se arquivo existe"""
    if os.path.exists(filepath):
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} NÃO ENCONTRADO: {filepath}")
        return False

def check_version_json():
    """Valida VERSION.json"""
    print_header("Validando VERSION.json")
    
    filepath = 'esp32/VERSION.json'
    if not check_file_exists(filepath, "VERSION.json"):
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            version_data = json.load(f)
        
        # Validar campos obrigatórios
        required_fields = ['project', 'version', 'release_date', 'status', 'changes']
        for field in required_fields:
            if field in version_data:
                print_success(f"Campo '{field}': {version_data.get(field, 'N/A')}")
            else:
                print_error(f"Campo obrigatório '{field}' ausente")
                return False
        
        # Validar formato de versão (X.Y.Z)
        version = version_data.get('version', '')
        parts = version.split('.')
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            print_success(f"Formato de versão válido: {version}")
        else:
            print_error(f"Formato de versão inválido: {version}")
            return False
        
        # Verificar status
        status = version_data.get('status', '')
        valid_statuses = ['alpha', 'beta', 'rc', 'stable']
        if status in valid_statuses:
            print_success(f"Status válido: {status}")
        else:
            print_warning(f"Status desconhecido: {status}")
        
        print_success("VERSION.json válido!")
        return True
        
    except json.JSONDecodeError as e:
        print_error(f"Erro ao parsear JSON: {e}")
        return False
    except Exception as e:
        print_error(f"Erro ao validar VERSION.json: {e}")
        return False

def check_watchdog_implementation():
    """Verifica se watchdog foi implementado"""
    print_header("Validando Implementação de Watchdog")
    
    files_to_check = {
        'esp32/dashboard.py': [
            'from machine import WDT',
            'wdt = WDT(timeout=10000)',
            'wdt.feed()'
        ],
        'esp32/setup_wifi.py': [
            'from machine import WDT',
            'wdt = WDT(timeout=10000)',
            'wdt.feed()'
        ]
    }
    
    all_valid = True
    
    for filepath, patterns in files_to_check.items():
        print(f"\n[Arquivo] Verificando {filepath}...")
        
        if not os.path.exists(filepath):
            print_error(f"Arquivo não encontrado: {filepath}")
            all_valid = False
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for pattern in patterns:
            if pattern in content:
                print_success(f"Encontrado: {pattern}")
            else:
                print_error(f"NÃO encontrado: {pattern}")
                all_valid = False
    
    if all_valid:
        print_success("\nWatchdog implementado corretamente em ambos arquivos!")
    else:
        print_error("\nWatchdog incompleto ou ausente")
    
    return all_valid

def check_indentation_fix():
    """Verifica se bug de indentação foi corrigido"""
    print_header("Validando Correção de Bug de Indentação")
    
    filepath = 'esp32/setup_wifi.py'
    
    if not os.path.exists(filepath):
        print_error(f"Arquivo não encontrado: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Procurar pela linha problemática
    # Deve ter "elif '/css/base.css'" no mesmo nível de indentação que outros "elif"
    
    found_issue = False
    for i, line in enumerate(lines, 1):
        if "elif '/css/base.css'" in line:
            # Verificar se está no nível correto (12 espaços ou 3 tabs)
            indent = len(line) - len(line.lstrip())
            if indent == 12 or line.startswith('            elif'):
                print_success(f"Linha {i}: Indentação correta para 'elif /css/base.css'")
                return True
            else:
                print_error(f"Linha {i}: Indentação INCORRETA ({indent} espaços)")
                found_issue = True
    
    if not found_issue:
        print_warning("Linha 'elif /css/base.css' não encontrada (arquivo pode ter mudado)")
        return True  # Não considera erro se não encontrou
    
    return False

def check_changelog():
    """Verifica se CHANGELOG foi atualizado"""
    print_header("Validando CHANGELOG.md")
    
    filepath = 'esp32/CHANGELOG.md'
    if not check_file_exists(filepath, "CHANGELOG.md"):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se versão atual está documentada
    with open('esp32/VERSION.json', 'r', encoding='utf-8') as f:
        version_data = json.load(f)
        version = version_data.get('version', '')
    
    if f"[{version}]" in content:
        print_success(f"Versão {version} documentada no CHANGELOG")
    else:
        print_error(f"Versão {version} NÃO encontrada no CHANGELOG")
        return False
    
    # Verificar se tem seção de mudanças
    keywords = ['watchdog', 'indentação', 'bug', 'fix', 'correção']
    found_keywords = []
    for keyword in keywords:
        if keyword.lower() in content.lower():
            found_keywords.append(keyword)
    
    if found_keywords:
        print_success(f"Palavras-chave encontradas: {', '.join(found_keywords)}")
    else:
        print_warning("Nenhuma palavra-chave de mudanças encontrada")
    
    print_success("CHANGELOG.md validado!")
    return True

def check_core_files():
    """Verifica se arquivos core existem"""
    print_header("Validando Arquivos Core")
    
    core_files = [
        ('esp32/boot.py', 'Boot Script'),
        ('esp32/main.py', 'Main Script'),
        ('esp32/dashboard.py', 'Dashboard Server'),
        ('esp32/setup_wifi.py', 'Setup WiFi Server'),
        ('esp32/data/config.json', 'Configuração'),
        ('esp32/data/sensors.json', 'Dados de Sensores'),
        ('esp32/data/sensors_config.json', 'Config de Sensores'),
        ('esp32/web/index.html', 'Dashboard HTML'),
        ('esp32/web/config.html', 'Config HTML'),
        ('esp32/web/setup_wifi.html', 'Setup HTML'),
        ('esp32/web/css/base.css', 'Base CSS'),
        ('esp32/web/js/dashboard.js', 'Dashboard JS'),
        ('esp32/web/js/config.js', 'Config JS'),
        ('esp32/web/js/setup_wifi.js', 'Setup JS'),
    ]
    
    all_exist = True
    for filepath, description in core_files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    if all_exist:
        print_success("\nTodos os arquivos core presentes!")
    else:
        print_error("\nAlguns arquivos core estão faltando")
    
    return all_exist

def check_documentation():
    """Verifica se documentação existe"""
    print_header("Validando Documentação")
    
    doc_files = [
        ('README.md', 'README Principal'),
        ('esp32/CHANGELOG.md', 'CHANGELOG'),
        ('esp32/VERSION.json', 'VERSION Manifest'),
        ('ANALISE_COMPLETA_PROJETO.md', 'Análise Completa'),
        ('docs/GUIA_RAPIDO.md', 'Guia Rápido'),
        ('docs/ESP32_ESTRUTURA.md', 'Estrutura ESP32'),
    ]
    
    all_exist = True
    for filepath, description in doc_files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    if all_exist:
        print_success("\nDocumentacao completa!")
    else:
        print_warning("\nAlguma documentacao esta faltando (nao critico)")
    
    return all_exist

def generate_release_summary():
    """Gera resumo da release"""
    print_header("Resumo da Release")
    
    try:
        with open('esp32/VERSION.json', 'r', encoding='utf-8') as f:
            version_data = json.load(f)
        
        print(f"{Colors.BOLD}Projeto:{Colors.END} {version_data.get('project', 'N/A')}")
        print(f"{Colors.BOLD}Versão:{Colors.END} {version_data.get('version', 'N/A')}")
        print(f"{Colors.BOLD}Codename:{Colors.END} {version_data.get('codename', 'N/A')}")
        print(f"{Colors.BOLD}Data:{Colors.END} {version_data.get('release_date', 'N/A')}")
        print(f"{Colors.BOLD}Status:{Colors.END} {version_data.get('status', 'N/A')}")
        print(f"{Colors.BOLD}Tipo:{Colors.END} {version_data.get('type', 'N/A')}")
        
        print(f"\n{Colors.BOLD}Mudanças:{Colors.END}")
        changes = version_data.get('changes', {})
        
        if 'added' in changes:
            print(f"\n{Colors.GREEN}Adicionado:{Colors.END}")
            for item in changes['added']:
                print(f"  • {item}")
        
        if 'fixed' in changes:
            print(f"\n{Colors.GREEN}Corrigido:{Colors.END}")
            for item in changes['fixed']:
                print(f"  • {item}")
        
        if 'security' in changes:
            print(f"\n{Colors.GREEN}Segurança:{Colors.END}")
            for item in changes['security']:
                print(f"  • {item}")
        
        print(f"\n{Colors.BOLD}Known Issues:{Colors.END}")
        issues = version_data.get('known_issues', [])
        for issue in issues:
            severity = issue.get('severity', 'unknown').upper()
            color = Colors.RED if severity == 'HIGH' else Colors.YELLOW if severity == 'MEDIUM' else Colors.BLUE
            print(f"  {color}[{severity}]{Colors.END} {issue.get('description', 'N/A')}")
        
        return True
        
    except Exception as e:
        print_error(f"Erro ao gerar resumo: {e}")
        return False

def main():
    """Função principal"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("="*62)
    print("        MONITOR MINER - VALIDACAO DE RELEASE v3.2.1        ")
    print("="*62)
    print(f"{Colors.END}\n")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('esp32'):
        print_error("Erro: Diretório 'esp32' não encontrado!")
        print_info("Execute este script na raiz do projeto Monitor Miner")
        sys.exit(1)
    
    # Executar validações
    results = {}
    
    results['version_json'] = check_version_json()
    results['watchdog'] = check_watchdog_implementation()
    results['indentation'] = check_indentation_fix()
    results['changelog'] = check_changelog()
    results['core_files'] = check_core_files()
    results['documentation'] = check_documentation()
    
    # Gerar resumo
    generate_release_summary()
    
    # Resultado final
    print_header("Resultado da Validação")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n{Colors.BOLD}Validações:{Colors.END}")
    for check, result in results.items():
        status = f"{Colors.GREEN}PASSOU{Colors.END}" if result else f"{Colors.RED}FALHOU{Colors.END}"
        print(f"  {check:20s}: {status}")
    
    print(f"\n{Colors.BOLD}Total:{Colors.END} {passed}/{total} validações passaram")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("="*62)
        print("                 RELEASE VALIDADA!                   ")
        print("                                                            ")
        print("        Pronta para commit e testes de campo!              ")
        print("="*62)
        print(f"{Colors.END}\n")
        
        print_info("Próximos passos:")
        print("  1. git add .")
        print("  2. git commit -m 'Release v3.2.1 - Watchdog & Bugfix'")
        print("  3. git tag v3.2.1")
        print("  4. Upload para ESP32 e testes")
        
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}")
        print("="*62)
        print("              VALIDACAO FALHOU!                       ")
        print("                                                            ")
        print("          Corrija os erros antes de commitar!               ")
        print("="*62)
        print(f"{Colors.END}\n")
        
        sys.exit(1)

if __name__ == '__main__':
    main()

