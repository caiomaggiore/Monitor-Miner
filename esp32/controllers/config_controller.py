# ============================================================================
# CONFIG CONTROLLER - Monitor Miner v4.0
# ============================================================================
# Controller que orquestra configurações
# - Coordena data_store para configurações
# - Processa requisições de configuração
# - Valida dados de configuração
# ============================================================================

from core.response import json_response, html_response, error_response
from services.data_store import data_store

class ConfigController:
    """
    Controller para configurações
    - Orquestra data_store
    - Processa requisições de configuração
    - Valida dados
    """
    
    def __init__(self):
        print("[CONTROLLER] ✅ Config Controller inicializado")
    
    def handle_config_request(self, request):
        """
        Processa requisição de configuração
        - request: dicionário com dados da requisição
        """
        try:
            method = request.get('method', 'GET')
            path = request.get('path', '/')
            
            print(f"[CONFIG] Processando: {method} {path}")
            
            # Roteamento básico
            if path == '/config' or path == '/config/':
                return self._serve_config_page()
            elif path == '/api/config':
                if method == 'GET':
                    return self._get_config()
                elif method == 'POST':
                    return self._update_config(request)
            elif path == '/api/sensors/config':
                if method == 'GET':
                    return self._get_sensors_config()
                elif method == 'POST':
                    return self._update_sensors_config(request)
            elif path.startswith('/api/sensors/'):
                if method == 'POST':
                    return self._add_sensor(request)
                elif method == 'DELETE':
                    sensor_id = path.split('/')[-1]
                    return self._remove_sensor(sensor_id)
            else:
                return self._serve_static_file(path)
                
        except Exception as e:
            print(f"[CONFIG] ❌ Erro: {e}")
            return error_response(f"Config error: {str(e)}")
    
    def _serve_config_page(self):
        """Serve página de configuração"""
        try:
            # Ler arquivo HTML
            with open('web/config.html', 'r') as f:
                html_content = f.read()
            
            return html_response(html_content)
            
        except Exception as e:
            print(f"[CONFIG] ❌ Erro ao servir página de configuração: {e}")
            return error_response("Página de configuração não disponível")
    
    def _get_config(self):
        """Retorna configuração geral"""
        try:
            # Obter configuração do data_store
            config = data_store.read_json("config")
            
            if config is None:
                # Configuração padrão
                config = {
                    'wifi': {
                        'ssid': '',
                        'password': '',
                        'auto_connect': True
                    },
                    'system': {
                        'hostname': 'MonitorMiner',
                        'timezone': 'America/Sao_Paulo',
                        'update_interval': 5
                    },
                    'sensors': {
                        'update_interval': 10,
                        'max_sensors': 10
                    }
                }
            
            return json_response(config)
            
        except Exception as e:
            print(f"[CONFIG] ❌ Erro ao obter configuração: {e}")
            return error_response("Erro ao obter configuração")
    
    def _update_config(self, request):
        """Atualiza configuração geral"""
        try:
            # Obter dados do request (simulado)
            # Em implementação real, extrair do body da requisição
            updates = {
                'wifi': {
                    'ssid': 'NovaRede',
                    'password': 'novaSenha123',
                    'auto_connect': True
                },
                'system': {
                    'hostname': 'MonitorMiner',
                    'timezone': 'America/Sao_Paulo',
                    'update_interval': 5
                }
            }
            
            # Atualizar configuração
            success = data_store.update_json("config", updates)
            
            if success:
                return json_response({"status": "success", "message": "Configuração atualizada"})
            else:
                return error_response("Erro ao atualizar configuração")
            
        except Exception as e:
            print(f"[CONFIG] ❌ Erro ao atualizar configuração: {e}")
            return error_response("Erro ao atualizar configuração")
    
    def _get_sensors_config(self):
        """Retorna configuração de sensores"""
        try:
            # Obter configuração de sensores
            sensors_config = data_store.get_sensors_config()
            
            if sensors_config is None:
                # Configuração padrão
                sensors_config = {
                    'sensors': [],
                    'settings': {
                        'update_interval': 10,
                        'max_sensors': 10,
                        'auto_discovery': True
                    }
                }
            
            return json_response(sensors_config)
            
        except Exception as e:
            print(f"[CONFIG] ❌ Erro ao obter configuração de sensores: {e}")
            return error_response("Erro ao obter configuração de sensores")
    
    def _update_sensors_config(self, request):
        """Atualiza configuração de sensores"""
        try:
            # Obter dados do request (simulado)
            updates = {
                'settings': {
                    'update_interval': 15,
                    'max_sensors': 15,
                    'auto_discovery': True
                }
            }
            
            # Atualizar configuração
            success = data_store.update_json("sensors_config", updates)
            
            if success:
                return json_response({"status": "success", "message": "Configuração de sensores atualizada"})
            else:
                return error_response("Erro ao atualizar configuração de sensores")
            
        except Exception as e:
            print(f"[CONFIG] ❌ Erro ao atualizar configuração de sensores: {e}")
            return error_response("Erro ao atualizar configuração de sensores")
    
    def _add_sensor(self, request):
        """Adiciona novo sensor"""
        try:
            # Obter dados do request (simulado)
            new_sensor = {
                'id': 'temp_2',
                'name': 'Temperatura Externa',
                'type': 'temperature',
                'pin': 2,
                'enabled': True
            }
            
            # Obter configuração atual
            sensors_config = data_store.get_sensors_config()
            if sensors_config is None:
                sensors_config = {'sensors': [], 'settings': {}}
            
            # Adicionar novo sensor
            if 'sensors' not in sensors_config:
                sensors_config['sensors'] = []
            
            sensors_config['sensors'].append(new_sensor)
            
            # Salvar configuração
            success = data_store.save_sensors_config(sensors_config)
            
            if success:
                return json_response({"status": "success", "message": "Sensor adicionado", "sensor": new_sensor})
            else:
                return error_response("Erro ao adicionar sensor")
            
        except Exception as e:
            print(f"[CONFIG] ❌ Erro ao adicionar sensor: {e}")
            return error_response("Erro ao adicionar sensor")
    
    def _remove_sensor(self, sensor_id):
        """Remove sensor"""
        try:
            # Obter configuração atual
            sensors_config = data_store.get_sensors_config()
            if sensors_config is None:
                return error_response("Configuração de sensores não encontrada")
            
            # Remover sensor
            if 'sensors' in sensors_config:
                sensors = sensors_config['sensors']
                sensors_config['sensors'] = [s for s in sensors if s.get('id') != sensor_id]
            
            # Salvar configuração
            success = data_store.save_sensors_config(sensors_config)
            
            if success:
                return json_response({"status": "success", "message": f"Sensor {sensor_id} removido"})
            else:
                return error_response("Erro ao remover sensor")
            
        except Exception as e:
            print(f"[CONFIG] ❌ Erro ao remover sensor {sensor_id}: {e}")
            return error_response(f"Erro ao remover sensor {sensor_id}")
    
    def _serve_static_file(self, path):
        """Serve arquivo estático"""
        try:
            # Remover barra inicial
            if path.startswith('/'):
                path = path[1:]
            
            # Ler arquivo
            with open(f'web/{path}', 'r') as f:
                content = f.read()
            
            return html_response(content)
            
        except FileNotFoundError:
            return error_response("Arquivo não encontrado", 404)
        except Exception as e:
            print(f"[CONFIG] ❌ Erro ao servir arquivo {path}: {e}")
            return error_response(f"Erro ao servir arquivo: {str(e)}")
    
    def get_stats(self):
        """Retorna estatísticas do controller"""
        return {
            'controller': 'config',
            'version': '4.0.0',
            'data_store_stats': data_store.get_cache_stats()
        }

# Instância global do controller
config_controller = ConfigController()

# Função de conveniência
def handle_config_request(request):
    """Função de conveniência"""
    return config_controller.handle_config_request(request)
