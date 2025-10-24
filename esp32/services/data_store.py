# ============================================================================
# DATA STORE SERVICE - Monitor Miner v4.0
# ============================================================================
# Serviço para acesso a dados JSON
# - Leitura/escrita de arquivos JSON
# - Cache de dados
# - Validação de dados
# ============================================================================

import json
import os

class DataStoreService:
    """
    Serviço para acesso a dados JSON
    - Cache de arquivos JSON
    - Validação de dados
    - Operações CRUD
    """
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.cache = {}
        self.cache_max_size = 10
        
        # Criar diretório se não existir
        try:
            os.makedirs(data_dir, exist_ok=True)
        except:
            pass  # MicroPython pode não ter makedirs
        
        print(f"[SERVICE] ✅ Data Store Service inicializado (dir: {data_dir})")
    
    def read_json(self, filename):
        """
        Lê arquivo JSON com cache
        - filename: nome do arquivo (sem extensão .json)
        """
        try:
            # Verificar cache
            if filename in self.cache:
                print(f"[DATA] 📁 Cache hit: {filename}")
                return self.cache[filename]
            
            # Caminho do arquivo
            filepath = f"{self.data_dir}/{filename}.json"
            
            # Ler arquivo
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Adicionar ao cache
            self._add_to_cache(filename, data)
            
            print(f"[DATA] 📁 Arquivo lido: {filename}")
            return data
            
        except FileNotFoundError:
            print(f"[DATA] ❌ Arquivo não encontrado: {filename}")
            return None
        except json.JSONDecodeError as e:
            print(f"[DATA] ❌ Erro JSON em {filename}: {e}")
            return None
        except Exception as e:
            print(f"[DATA] ❌ Erro ao ler {filename}: {e}")
            return None
    
    def write_json(self, filename, data):
        """
        Escreve arquivo JSON
        - filename: nome do arquivo (sem extensão .json)
        - data: dados para escrever
        """
        try:
            # Caminho do arquivo
            filepath = f"{self.data_dir}/{filename}.json"
            
            # Escrever arquivo
            with open(filepath, 'w') as f:
                json.dump(data, f, separators=(',', ':'))  # Compact JSON
            
            # Atualizar cache
            self._add_to_cache(filename, data)
            
            print(f"[DATA] 💾 Arquivo escrito: {filename}")
            return True
            
        except Exception as e:
            print(f"[DATA] ❌ Erro ao escrever {filename}: {e}")
            return False
    
    def update_json(self, filename, updates):
        """
        Atualiza arquivo JSON existente
        - filename: nome do arquivo
        - updates: dicionário com atualizações
        """
        try:
            # Ler dados existentes
            data = self.read_json(filename)
            if data is None:
                data = {}
            
            # Aplicar atualizações
            if isinstance(data, dict) and isinstance(updates, dict):
                data.update(updates)
            else:
                print(f"[DATA] ❌ Dados não são dicionários: {filename}")
                return False
            
            # Escrever dados atualizados
            return self.write_json(filename, data)
            
        except Exception as e:
            print(f"[DATA] ❌ Erro ao atualizar {filename}: {e}")
            return False
    
    def delete_json(self, filename):
        """
        Remove arquivo JSON
        - filename: nome do arquivo
        """
        try:
            filepath = f"{self.data_dir}/{filename}.json"
            
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"[DATA] 🗑️ Arquivo removido: {filename}")
                
                # Remover do cache
                if filename in self.cache:
                    del self.cache[filename]
                
                return True
            else:
                print(f"[DATA] ❌ Arquivo não existe: {filename}")
                return False
                
        except Exception as e:
            print(f"[DATA] ❌ Erro ao remover {filename}: {e}")
            return False
    
    def list_files(self):
        """
        Lista todos os arquivos JSON no diretório
        """
        try:
            files = []
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    files.append(filename[:-5])  # Remove .json
            return files
        except Exception as e:
            print(f"[DATA] ❌ Erro ao listar arquivos: {e}")
            return []
    
    def _add_to_cache(self, filename, data):
        """Adiciona dados ao cache (LRU)"""
        # Se cache está cheio, remover item mais antigo
        if len(self.cache) >= self.cache_max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[filename] = data
    
    def clear_cache(self):
        """Limpa o cache"""
        self.cache.clear()
        print("[DATA] 🧹 Cache limpo")
    
    def get_cache_stats(self):
        """Retorna estatísticas do cache"""
        return {
            'size': len(self.cache),
            'max_size': self.cache_max_size,
            'files': list(self.cache.keys())
        }
    
    def validate_json(self, data, schema=None):
        """
        Valida dados JSON (implementação básica)
        - data: dados para validar
        - schema: esquema de validação (opcional)
        """
        try:
            # Validação básica
            if not isinstance(data, (dict, list)):
                return False, "Dados devem ser dict ou list"
            
            # Validação por schema (implementação básica)
            if schema:
                if isinstance(schema, dict) and isinstance(data, dict):
                    for key, expected_type in schema.items():
                        if key in data:
                            if not isinstance(data[key], expected_type):
                                return False, f"Campo '{key}' deve ser {expected_type.__name__}"
            
            return True, "Dados válidos"
            
        except Exception as e:
            return False, f"Erro de validação: {e}"

# Instância global do serviço
data_store = DataStoreService()

# Funções de conveniência
def read_config(filename):
    """Lê configuração"""
    return data_store.read_json(filename)

def write_config(filename, data):
    """Escreve configuração"""
    return data_store.write_json(filename, data)

def update_config(filename, updates):
    """Atualiza configuração"""
    return data_store.update_json(filename, updates)

def get_sensors_config():
    """Lê configuração de sensores"""
    return data_store.read_json("sensors_config")

def save_sensors_config(data):
    """Salva configuração de sensores"""
    return data_store.write_json("sensors_config", data)

def get_sensors_data():
    """Lê dados dos sensores"""
    return data_store.read_json("sensors")

def save_sensors_data(data):
    """Salva dados dos sensores"""
    return data_store.write_json("sensors", data)
