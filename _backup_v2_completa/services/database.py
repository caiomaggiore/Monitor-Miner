"""
Database - Sistema de persistência JSON
"""

import json

class Database:
    def __init__(self, base_path='data'):
        self.base_path = base_path
        self._ensure_data_dir()
        self._init_default_config()
    
    def _ensure_data_dir(self):
        """Garante que diretório data existe"""
        try:
            import os
            try:
                os.mkdir(self.base_path)
            except OSError:
                pass  # Diretório já existe
        except:
            pass
    
    def _init_default_config(self):
        """Inicializa configuração padrão se não existir"""
        try:
            self.load('config')
        except:
            default_config = {
                'wifi': {
                    'ssid': 'SuaRede',
                    'password': 'SuaSenha',
                    'use_dhcp': True,
                    'static_ip': '192.168.1.100',
                    'subnet_mask': '255.255.255.0',
                    'gateway': '192.168.1.1',
                    'dns': '8.8.8.8'
                },
                'sensors': {
                    'read_interval': 5,
                    'dht22_pin': 23,
                    'dht11_pin': 22
                },
                'relays': {
                    'pins': [25, 26, 32, 27]
                },
                'automation': {
                    'enabled': False
                }
            }
            self.save('config', default_config)
    
    def load(self, name):
        """Carrega JSON do arquivo"""
        file_path = f'{self.base_path}/{name}.json'
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Erro ao carregar {name}: {e}")
    
    def save(self, name, data):
        """Salva JSON no arquivo"""
        file_path = f'{self.base_path}/{name}.json'
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            raise Exception(f"Erro ao salvar {name}: {e}")
    
    def exists(self, name):
        """Verifica se arquivo existe"""
        file_path = f'{self.base_path}/{name}.json'
        try:
            import os
            os.stat(file_path)
            return True
        except:
            return False
    
    def delete(self, name):
        """Deleta arquivo"""
        file_path = f'{self.base_path}/{name}.json'
        try:
            import os
            os.remove(file_path)
            return True
        except:
            return False

