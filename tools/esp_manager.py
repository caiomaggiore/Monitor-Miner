#!/usr/bin/env python3
"""
ESP32 Manager - CLI para gerenciamento do projeto ESP32
Monitor Miner v2.0
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import hashlib

# Adicionar pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configuração da porta
try:
    from port_config import ESP32_PORT
except ImportError:
    ESP32_PORT = "COM5"
    print("⚠️ config.py não encontrado, usando COM5 como padrão")


class ESP32Manager:
    """Gerenciador CLI para ESP32"""
    
    def __init__(self):
        self.port = ESP32_PORT
        self.connected = False
        self.project_root = Path(__file__).parent.parent
        self.esp32_dir = self.project_root / "esp32"
        self.espignore_file = self.project_root / ".espignore"
        self.espignore_patterns = self.load_espignore()
        
    def load_espignore(self):
        """Carrega padrões do .espignore"""
        patterns = []
        if self.espignore_file.exists():
            with open(self.espignore_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
        return patterns
    
    def run_cmd(self, cmd, timeout=30, show_output=True):
        """Executa comando e retorna resultado"""
        try:
            if show_output:
                print(f"🔄 Executando...")
            
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                if show_output and result.stdout.strip():
                    print(result.stdout.strip())
                return True, result.stdout.strip()
            else:
                if show_output:
                    print(f"❌ Erro: {result.stderr.strip()}")
                return False, result.stderr.strip()
                
        except subprocess.TimeoutExpired:
            if show_output:
                print("⏰ Timeout")
            return False, "Timeout"
        except Exception as e:
            if show_output:
                print(f"💥 Erro: {e}")
            return False, str(e)
    
    def check_connection(self, silent=False):
        """Verifica conexão com ESP32"""
        cmd = f'python -m mpremote connect {self.port} exec "print(\'OK\')"'
        success, _ = self.run_cmd(cmd, timeout=5, show_output=not silent)
        self.connected = success
        return success
    
    def get_esp32_status(self):
        """Obtém status do ESP32"""
        if not self.connected:
            return "❌ Desconectado"
        
        # Tentar obter informações
        cmd = f'python -m mpremote connect {self.port} exec "import os; stat = os.statvfs(\'/\'); print(stat[3] * stat[0])"'
        success, output = self.run_cmd(cmd, timeout=10, show_output=False)
        
        if success and output:
            try:
                bytes_free = int(output)
                mb_free = bytes_free / (1024 * 1024)
                return f"✅ Conectado | {mb_free:.2f}MB livre"
            except:
                pass
        
        return "✅ Conectado"
    
    def clear_screen(self):
        """Limpa a tela"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Imprime cabeçalho"""
        self.clear_screen()
        print("=" * 60)
        print("🔧 ESP32 Manager - Monitor Miner v2.0")
        print("=" * 60)
        print(f"Porta: {self.port}")
        print(f"Status: {self.get_esp32_status()}")
        print(f"Projeto: {self.esp32_dir}")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Imprime menu de opções"""
        print("📋 OPÇÕES:")
        print()
        print("  [1] 📤 Upload Completo (esp32/)")
        print("  [2] 📁 Upload Seletivo")
        print("  [3] 📊 Diagnóstico")
        print("  [4] 🔄 Reiniciar ESP32")
        print("  [5] 💾 Verificar Espaço")
        print("  [6] 📜 Ver Arquivos ESP32")
        print("  [7] 🖥️  REPL Interativo")
        print("  [8] 📺 Monitor de Logs (com reset)")
        print("  [9] 🧹 Formatar ESP32")
        print("  [t] 🔌 Testar Conexão")
        print("  [0] ℹ️  Sobre")
        print()
        print("  [q] ❌ Sair")
        print()
    
    def directory_exists(self, dir_path):
        """Verifica se diretório existe na ESP32"""
        # Usar comando fs ls para verificar
        cmd = f'python -m mpremote connect {self.port} fs ls :{dir_path}'
        success, output = self.run_cmd(cmd, timeout=10, show_output=False)
        
        # Se comando teve sucesso, diretório existe
        return success
    
    def create_directory(self, dir_path):
        """Cria diretório na ESP32 usando fs mkdir"""
        # Verificar se já existe
        if self.directory_exists(dir_path):
            return True
        
        # Usar comando fs mkdir nativo do mpremote
        cmd = f'python -m mpremote connect {self.port} fs mkdir :{dir_path}'
        success, output = self.run_cmd(cmd, timeout=10, show_output=False)
        
        if not success:
            # Se falhou, pode ser que o pai não existe, retornar False
            return False
        
        # Validar se foi criado
        return self.directory_exists(dir_path)
    
    def create_directory_recursive(self, dir_path):
        """Cria diretório recursivamente (pai primeiro)"""
        parts = dir_path.split('/')
        current = ""
        
        for part in parts:
            if current:
                current += "/" + part
            else:
                current = part
            
            if not self.create_directory(current):
                return False
        
        return True
    
    def get_all_files(self):
        """Lista todos os arquivos do projeto esp32/"""
        all_files = []
        
        # Procurar todos os arquivos
        for ext in ['*.py', '*.html', '*.css', '*.js', '*.json']:
            files = list(self.esp32_dir.rglob(ext))
            all_files.extend(files)
        
        return all_files
    
    def upload_file_with_dirs(self, local_file, remote_path):
        """Upload arquivo criando diretórios necessários"""
        # Verificar se arquivo local existe
        if not local_file.exists():
            return False, f"Arquivo local não encontrado: {local_file}"
        
        # Criar diretórios pai se necessário
        remote_parts = remote_path.split('/')
        if len(remote_parts) > 1:
            dir_path = '/'.join(remote_parts[:-1])
            
            # Tentar criar diretório recursivamente
            if not self.create_directory_recursive(dir_path):
                return False, f"Não foi possível criar diretório: {dir_path}"
        
        # Fazer upload do arquivo
        cmd = f'python -m mpremote connect {self.port} fs cp "{local_file}" ":{remote_path}"'
        success, output = self.run_cmd(cmd, timeout=30, show_output=False)
        
        if not success:
            # Extrair mensagem de erro mais clara
            error_msg = output if output else "Erro desconhecido"
            return False, error_msg
        
        return True, "OK"
    
    def upload_complete(self):
        """Upload completo da pasta esp32/ (inteligente)"""
        print("\n📤 Upload Completo (Inteligente)")
        print("=" * 60)
        
        if not self.esp32_dir.exists():
            print("❌ Pasta esp32/ não encontrada!")
            input("\nPressione Enter para continuar...")
            return
        
        # Listar todos os arquivos
        print("📊 Analisando arquivos...")
        all_files = self.get_all_files()
        
        if not all_files:
            print("❌ Nenhum arquivo encontrado em esp32/")
            input("\nPressione Enter para continuar...")
            return
        
        # Organizar por tipo
        files_by_type = {}
        for file in all_files:
            ext = file.suffix
            if ext not in files_by_type:
                files_by_type[ext] = []
            files_by_type[ext].append(file)
        
        # Mostrar resumo
        print(f"\n📁 Total de arquivos: {len(all_files)}")
        for ext, files in sorted(files_by_type.items()):
            print(f"  {ext or 'sem extensão'}: {len(files)} arquivo(s)")
        
        print("\n📋 Estrutura de diretórios:")
        dirs = set()
        for file in all_files:
            rel_path = file.relative_to(self.esp32_dir)
            if rel_path.parent != Path('.'):
                dirs.add(str(rel_path.parent).replace('\\', '/'))
        
        for d in sorted(dirs):
            print(f"  📂 {d}")
        
        print()
        confirm = input("Continuar com upload? [s/N]: ").lower()
        if confirm != 's':
            print("❌ Upload cancelado")
            input("\nPressione Enter para continuar...")
            return
        
        # Criar estrutura de diretórios
        print("\n📂 Criando estrutura de diretórios...")
        failed_dirs = []
        
        for d in sorted(dirs):
            print(f"  📁 {d}... ", end='', flush=True)
            
            if self.create_directory_recursive(d):
                print("✅")
            else:
                print("❌")
                failed_dirs.append(d)
        
        # Avisar se alguma pasta falhou
        if failed_dirs:
            print(f"\n⚠️  {len(failed_dirs)} diretório(s) não foram criados:")
            for d in failed_dirs:
                print(f"  ❌ {d}")
            
            print("\n💡 O ESP32 pode não suportar pastas aninhadas neste modo.")
            print("   Arquivos nessas pastas podem falhar no upload.")
            print()
            
            continue_anyway = input("Continuar mesmo assim? [s/N]: ").lower()
            if continue_anyway != 's':
                print("❌ Upload cancelado")
                input("\nPressione Enter para continuar...")
                return
        
        # Fazer upload dos arquivos
        print("\n📤 Enviando arquivos...")
        success_count = 0
        failed_files = []
        
        for idx, file in enumerate(all_files, 1):
            rel_path = file.relative_to(self.esp32_dir)
            remote_path = str(rel_path).replace('\\', '/')
            
            # Mostrar progresso
            print(f"\r[{idx}/{len(all_files)}] {remote_path[:50]:<50}", end='', flush=True)
            
            success, msg = self.upload_file_with_dirs(file, remote_path)
            
            if success:
                success_count += 1
            else:
                failed_files.append((remote_path, msg))
        
        print()  # Nova linha após progresso
        
        # Mostrar resultado
        print("\n" + "=" * 60)
        print(f"✅ Upload concluído: {success_count}/{len(all_files)} arquivos enviados")
        
        if failed_files:
            print(f"\n⚠️  {len(failed_files)} arquivo(s) com erro:")
            for file, msg in failed_files[:5]:  # Mostrar apenas os 5 primeiros
                print(f"  ❌ {file}")
                if msg:
                    print(f"     Erro: {msg[:60]}")
            
            if len(failed_files) > 5:
                print(f"  ... e mais {len(failed_files) - 5} arquivo(s)")
        
        # Verificar espaço final
        print("\n💾 Espaço após upload:")
        cmd = f'python -m mpremote connect {self.port} exec "import os; stat = os.statvfs(\'/\'); free = stat[3] * stat[0]; print(f\'{{free/1024/1024:.2f}}MB livres\')"'
        self.run_cmd(cmd, timeout=10)
        
        # Perguntar se quer reiniciar
        print()
        restart = input("Reiniciar ESP32? [S/n]: ").lower()
        if restart != 'n':
            print("\n🔄 Reiniciando ESP32...")
            self.run_cmd(f'python -m mpremote connect {self.port} reset', timeout=10)
            print("✅ ESP32 reiniciado!")
        
        input("\n✅ Pressione Enter para continuar...")
    
    def upload_selective(self):
        """Upload seletivo de arquivos"""
        print("\n📁 Upload Seletivo")
        print("=" * 60)
        
        if not self.esp32_dir.exists():
            print("❌ Pasta esp32/ não encontrada!")
            input("\nPressione Enter para continuar...")
            return
        
        # Listar arquivos Python na pasta esp32
        py_files = list(self.esp32_dir.rglob("*.py"))
        html_files = list(self.esp32_dir.rglob("*.html"))
        css_files = list(self.esp32_dir.rglob("*.css"))
        js_files = list(self.esp32_dir.rglob("*.js"))
        
        all_files = py_files + html_files + css_files + js_files
        
        if not all_files:
            print("❌ Nenhum arquivo encontrado em esp32/")
            input("\nPressione Enter para continuar...")
            return
        
        # Mostrar arquivos
        print("Arquivos disponíveis:")
        print()
        for idx, file in enumerate(all_files, 1):
            rel_path = file.relative_to(self.esp32_dir)
            print(f"  [{idx:2d}] {rel_path}")
        
        print()
        print("Digite os números dos arquivos separados por espaço (ex: 1 3 5)")
        print("Ou 'all' para todos os arquivos")
        selection = input("Seleção: ").strip()
        
        if not selection:
            print("❌ Nenhum arquivo selecionado")
            input("\nPressione Enter para continuar...")
            return
        
        # Processar seleção
        selected_files = []
        if selection.lower() == 'all':
            selected_files = all_files
        else:
            try:
                indices = [int(x) - 1 for x in selection.split()]
                selected_files = [all_files[i] for i in indices if 0 <= i < len(all_files)]
            except:
                print("❌ Seleção inválida")
                input("\nPressione Enter para continuar...")
                return
        
        if not selected_files:
            print("❌ Nenhum arquivo selecionado")
            input("\nPressione Enter para continuar...")
            return
        
        # Identificar diretórios necessários
        dirs_needed = set()
        for file in selected_files:
            rel_path = file.relative_to(self.esp32_dir)
            if rel_path.parent != Path('.'):
                dir_path = str(rel_path.parent).replace('\\', '/')
                dirs_needed.add(dir_path)
        
        # Criar diretórios se necessário
        if dirs_needed:
            print(f"\n📂 Criando {len(dirs_needed)} diretório(s)...")
            failed_dirs = []
            
            for d in sorted(dirs_needed):
                print(f"  📁 {d}... ", end='', flush=True)
                
                if self.create_directory_recursive(d):
                    print("✅")
                else:
                    print("❌")
                    failed_dirs.append(d)
            
            if failed_dirs:
                print(f"\n⚠️  {len(failed_dirs)} diretório(s) não foram criados!")
                for d in failed_dirs:
                    print(f"  ❌ {d}")
                
                print("\n💡 Arquivos nessas pastas podem falhar no upload.")
                input("\nPressione Enter para continuar...")
        
        # Fazer upload
        print(f"\n📤 Enviando {len(selected_files)} arquivo(s)...")
        success_count = 0
        failed_files = []
        
        for idx, file in enumerate(selected_files, 1):
            rel_path = file.relative_to(self.esp32_dir)
            remote_path = str(rel_path).replace('\\', '/')
            
            print(f"  [{idx}/{len(selected_files)}] {rel_path}... ", end='', flush=True)
            
            success, msg = self.upload_file_with_dirs(file, remote_path)
            
            if success:
                print("✅")
                success_count += 1
            else:
                print("❌")
                failed_files.append((remote_path, msg))
        
        # Mostrar resultado
        print("\n" + "=" * 60)
        print(f"✅ Upload concluído: {success_count}/{len(selected_files)} arquivos enviados")
        
        if failed_files:
            print(f"\n⚠️  {len(failed_files)} arquivo(s) com erro:")
            for file, msg in failed_files:
                print(f"  ❌ {file}")
                if msg:
                    print(f"     Erro: {msg[:60]}")
        
        input("\n✅ Pressione Enter para continuar...")
    
    def diagnose(self):
        """Executa diagnóstico"""
        print("\n🔍 Diagnóstico ESP32")
        print("=" * 60)
        
        # Versão MicroPython
        print("\n🐍 Versão MicroPython:")
        cmd = f'python -m mpremote connect {self.port} exec "import sys; print(sys.version)"'
        self.run_cmd(cmd, timeout=10)
        
        # Espaço em disco
        print("\n💾 Espaço em disco:")
        cmd = f'python -m mpremote connect {self.port} exec "import os; stat = os.statvfs(\'/\'); free = stat[3] * stat[0]; total = stat[2] * stat[0]; print(f\'Livre: {{free/1024/1024:.2f}}MB / Total: {{total/1024/1024:.2f}}MB\')"'
        self.run_cmd(cmd, timeout=10)
        
        # Memória RAM
        print("\n🧠 Memória RAM:")
        cmd = f'python -m mpremote connect {self.port} exec "import gc; print(f\'RAM livre: {{gc.mem_free()/1024:.2f}}KB\')"'
        self.run_cmd(cmd, timeout=10)
        
        # Arquivos
        print("\n📁 Arquivos na raiz:")
        cmd = f'python -m mpremote connect {self.port} exec "import os; print(\'\\n\'.join(os.listdir(\'.\')))"'
        self.run_cmd(cmd, timeout=10)
        
        input("\n✅ Pressione Enter para continuar...")
    
    def restart_esp32(self):
        """Reinicia ESP32"""
        print("\n🔄 Reiniciando ESP32...")
        cmd = f'python -m mpremote connect {self.port} reset'
        success, _ = self.run_cmd(cmd, timeout=10)
        
        if success:
            print("✅ ESP32 reiniciado!")
            time.sleep(2)
        else:
            print("❌ Erro ao reiniciar")
        
        input("\nPressione Enter para continuar...")
    
    def check_space(self):
        """Verifica espaço disponível"""
        print("\n💾 Espaço Disponível")
        print("=" * 60)
        
        cmd = f'python -m mpremote connect {self.port} exec "import os; stat = os.statvfs(\'/\'); free = stat[3] * stat[0]; used = (stat[2] - stat[3]) * stat[0]; total = stat[2] * stat[0]; print(f\'Total: {{total/1024/1024:.2f}}MB\'); print(f\'Usado: {{used/1024/1024:.2f}}MB\'); print(f\'Livre: {{free/1024/1024:.2f}}MB\'); print(f\'Uso: {{used/total*100:.1f}}%\')"'
        self.run_cmd(cmd, timeout=10)
        
        input("\n✅ Pressione Enter para continuar...")
    
    def list_files(self):
        """Lista arquivos do ESP32"""
        print("\n📜 Arquivos no ESP32")
        print("=" * 60)
        
        # Listar raiz
        print("\n📂 Raiz (/):")
        cmd = f'python -m mpremote connect {self.port} fs ls'
        self.run_cmd(cmd, timeout=10)
        
        # Tentar listar subpastas comuns
        common_dirs = ['hardware', 'services', 'web', 'data']
        
        for dir_name in common_dirs:
            if self.directory_exists(dir_name):
                print(f"\n📂 {dir_name}/:")
                cmd = f'python -m mpremote connect {self.port} fs ls {dir_name}'
                self.run_cmd(cmd, timeout=10)
        
        input("\n✅ Pressione Enter para continuar...")
    
    def repl(self):
        """Abre REPL interativo"""
        print("\n🖥️  REPL Interativo")
        print("=" * 60)
        print("Use Ctrl+] para sair do REPL")
        print()
        print("💡 Dicas:")
        print("  • Ctrl+D - Soft reset (reinicia main.py)")
        print("  • Ctrl+C - Interrompe execução")
        print("  • Ctrl+] - Sai do REPL")
        print()
        input("Pressione Enter para continuar...")
        
        # Abrir REPL
        os.system(f'python -m mpremote connect {self.port} repl')
    
    def monitor_logs(self):
        """Monitor de logs com reset automático"""
        print("\n📺 Monitor de Logs")
        print("=" * 60)
        print("ESP32 será reiniciado e logs serão exibidos.")
        print("Use Ctrl+] para sair")
        print()
        input("Pressione Enter para continuar...")
        
        # Reiniciar e abrir REPL para ver logs
        print("\n🔄 Reiniciando ESP32...")
        os.system(f'python -m mpremote connect {self.port} reset repl')
    
    def format_esp32(self):
        """Formata ESP32"""
        print("\n🧹 Formatar ESP32")
        print("=" * 60)
        print("⚠️  ATENÇÃO: Isso vai APAGAR TUDO no ESP32!")
        print()
        confirm = input("Digite 'FORMATAR' para confirmar: ")
        
        if confirm != "FORMATAR":
            print("❌ Formatação cancelada")
            input("\nPressione Enter para continuar...")
            return
        
        print("\n🔄 Executando formatação...")
        
        # Executar script de formatação
        format_script = self.project_root / "tools" / "format_esp32_auto.py"
        if format_script.exists():
            os.system(f'python "{format_script}"')
        else:
            print("❌ Script de formatação não encontrado!")
        
        input("\n✅ Pressione Enter para continuar...")
    
    def about(self):
        """Mostra informações sobre o manager"""
        print("\nℹ️  Sobre o ESP32 Manager")
        print("=" * 60)
        print("Monitor Miner v2.0 - ESP32 Manager CLI")
        print()
        print("Ferramenta de gerenciamento para desenvolvimento ESP32")
        print()
        print("Recursos:")
        print("  • Upload completo e seletivo")
        print("  • Diagnóstico do sistema")
        print("  • Monitor de espaço e memória")
        print("  • REPL interativo")
        print("  • Formatação e reset")
        print()
        print(f"Porta configurada: {self.port}")
        print(f"Projeto: {self.esp32_dir}")
        print()
        print("Para alterar a porta, edite config.py")
        
        input("\n✅ Pressione Enter para continuar...")
    
    def run(self):
        """Loop principal do manager"""
        while True:
            # Verificar conexão
            if not self.connected:
                self.check_connection(silent=True)
            
            # Mostrar interface
            self.print_header()
            self.print_menu()
            
            # Obter escolha
            choice = input("Digite sua escolha: ").strip().lower()
            
            # Processar escolha
            if choice == '1':
                self.upload_complete()
            elif choice == '2':
                self.upload_selective()
            elif choice == '3':
                self.diagnose()
            elif choice == '4':
                self.restart_esp32()
            elif choice == '5':
                self.check_space()
            elif choice == '6':
                self.list_files()
            elif choice == '7':
                self.repl()
            elif choice == '8':
                self.monitor_logs()
            elif choice == '9':
                self.format_esp32()
            elif choice == 't':
                print("\n🔌 Testando conexão...")
                if self.check_connection():
                    print("✅ ESP32 conectado!")
                else:
                    print("❌ ESP32 não responde")
                input("\nPressione Enter para continuar...")
            elif choice == '0':
                self.about()
            elif choice == 'q':
                print("\n👋 Até logo!")
                break
            else:
                print("\n❌ Opção inválida!")
                time.sleep(1)


def main():
    """Função principal"""
    try:
        manager = ESP32Manager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!")
    except Exception as e:
        print(f"\n💥 Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

