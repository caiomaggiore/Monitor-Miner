# ============================================================================
# DASHBOARD CONTROLLER - Monitor Miner v4.0
# ============================================================================
# Controller que orquestra o dashboard
# - Coordena services (system_monitor, data_store)
# - Processa requisições do dashboard
# - Serve arquivos estáticos
# ============================================================================

from core.response import json_response, html_response, error_response
from services.system_monitor import system_monitor
from services.data_store import data_store

class DashboardController:
    """
    Controller para o dashboard
    - Orquestra services
    - Processa requisições
    - Serve arquivos estáticos
    """
    
    def __init__(self):
        print("[CONTROLLER] ✅ Dashboard Controller inicializado")
    
    def handle_dashboard_request(self, request):
        """
        Processa requisição do dashboard
        - request: dicionário com dados da requisição
        """
        try:
            method = request.get('method', 'GET')
            path = request.get('path', '/')
            
            print(f"[DASHBOARD] Processando: {method} {path}")
            
            # Roteamento básico
            if path == '/' or path == '/dashboard':
                return self._serve_dashboard()
            elif path == '/api/status':
                return self._get_system_status()
            elif path == '/api/sensors':
                return self._get_sensors_data()
            elif path.startswith('/api/sensors/'):
                sensor_id = path.split('/')[-1]
                return self._get_sensor_data(sensor_id)
            else:
                return self._serve_static_file(path)
                
        except Exception as e:
            print(f"[DASHBOARD] ❌ Erro: {e}")
            return error_response(f"Dashboard error: {str(e)}")
    
    def _serve_dashboard(self):
        """Serve página principal do dashboard"""
        try:
            # Ler arquivo HTML
            with open('web/index.html', 'r') as f:
                html_content = f.read()
            
            return html_response(html_content)
            
        except Exception as e:
            print(f"[DASHBOARD] ❌ Erro ao servir dashboard: {e}")
            return error_response("Dashboard não disponível")
    
    def _get_system_status(self):
        """Retorna status do sistema"""
        try:
            # Obter dados do system_monitor
            system_info = system_monitor.get_system_info()
            
            # Adicionar informações de rede (mock por enquanto)
            system_info['network'] = {
                'connected': True,
                'ip': '192.168.1.100',
                'ssid': 'MinhaRede',
                'signal': -45
            }
            
            return json_response(system_info)
            
        except Exception as e:
            print(f"[DASHBOARD] ❌ Erro ao obter status: {e}")
            return error_response("Erro ao obter status do sistema")
    
    def _get_sensors_data(self):
        """Retorna dados de todos os sensores"""
        try:
            # Obter dados dos sensores do data_store
            sensors_data = data_store.get_sensors_data()
            
            if sensors_data is None:
                # Dados mock se não existir arquivo
                sensors_data = {
                    'sensors': [
                        {
                            'id': 'temp_1',
                            'name': 'Temperatura Sala',
                            'type': 'temperature',
                            'value': 23.5,
                            'unit': '°C',
                            'status': 'online',
                            'last_update': 1640995200
                        },
                        {
                            'id': 'hum_1',
                            'name': 'Umidade Sala',
                            'type': 'humidity',
                            'value': 45.2,
                            'unit': '%',
                            'status': 'online',
                            'last_update': 1640995200
                        }
                    ],
                    'last_update': 1640995200
                }
            
            return json_response(sensors_data)
            
        except Exception as e:
            print(f"[DASHBOARD] ❌ Erro ao obter sensores: {e}")
            return error_response("Erro ao obter dados dos sensores")
    
    def _get_sensor_data(self, sensor_id):
        """Retorna dados de um sensor específico"""
        try:
            # Obter dados dos sensores
            sensors_data = data_store.get_sensors_data()
            
            if sensors_data is None:
                return error_response("Dados de sensores não encontrados")
            
            # Procurar sensor específico
            sensors = sensors_data.get('sensors', [])
            for sensor in sensors:
                if sensor.get('id') == sensor_id:
                    return json_response(sensor)
            
            return error_response(f"Sensor {sensor_id} não encontrado")
            
        except Exception as e:
            print(f"[DASHBOARD] ❌ Erro ao obter sensor {sensor_id}: {e}")
            return error_response(f"Erro ao obter dados do sensor {sensor_id}")
    
    def _serve_static_file(self, path):
        """Serve arquivo estático"""
        try:
            # Remover barra inicial
            if path.startswith('/'):
                path = path[1:]
            
            # Mapear extensões para content-type
            content_types = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.json': 'application/json',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.ico': 'image/x-icon'
            }
            
            # Detectar content-type
            content_type = 'text/plain'
            for ext, ctype in content_types.items():
                if path.endswith(ext):
                    content_type = ctype
                    break
            
            # Ler arquivo
            with open(f'web/{path}', 'r') as f:
                content = f.read()
            
            return html_response(content, content_type=content_type)
            
        except FileNotFoundError:
            return error_response("Arquivo não encontrado", 404)
        except Exception as e:
            print(f"[DASHBOARD] ❌ Erro ao servir arquivo {path}: {e}")
            return error_response(f"Erro ao servir arquivo: {str(e)}")
    
    def get_stats(self):
        """Retorna estatísticas do controller"""
        return {
            'controller': 'dashboard',
            'version': '4.0.0',
            'system_monitor_stats': system_monitor.get_stats(),
            'data_store_stats': data_store.get_cache_stats()
        }

# Instância global do controller
dashboard_controller = DashboardController()

# Função de conveniência
def handle_dashboard_request(request):
    """Função de conveniência"""
    return dashboard_controller.handle_dashboard_request(request)
