# ============================================================================
# MAIN v4.0 - Monitor Miner v4.0
# ============================================================================
# Arquitetura v4.0 - Modular e escalável
# - Core modules (http_server, router, response)
# - Services (system_monitor, data_store)
# - Controllers (dashboard, config)
# ============================================================================

import time
import gc
from machine import WDT

# Core modules
from core.http_server import HTTPServer
from core.router import Router
from core.response import json_response, error_response

# Services
from services.system_monitor import system_monitor
from services.data_store import data_store

# Controllers
from controllers.dashboard_controller import dashboard_controller
from controllers.config_controller import config_controller

class MonitorMinerApp:
    """
    Aplicação principal v4.0
    - Arquitetura modular
    - Services independentes
    - Controllers orquestradores
    """
    
    def __init__(self):
        self.http_server = None
        self.router = None
        self.wdt = None
        self.running = False
        
        print("[APP] 🚀 Inicializando Monitor Miner v4.0...")
    
    def initialize(self, mode='STA'):
        """Inicializa a aplicação"""
        try:
            # Inicializar servidor HTTP
            self.http_server = HTTPServer(host='0.0.0.0', port=8080)
            
            # Inicializar router
            self.router = Router()
            self._setup_routes()
            
            # Inicializar watchdog
            self.wdt = WDT(timeout=15)
            
            print(f"[APP] ✅ Aplicação inicializada (modo: {mode})")
            return True
            
        except Exception as e:
            print(f"[APP] ❌ Erro na inicialização: {e}")
            return False
    
    def _setup_routes(self):
        """Configura rotas da aplicação"""
        # Dashboard routes
        self.router.add_route('GET', '/', self._handle_dashboard)
        self.router.add_route('GET', '/dashboard', self._handle_dashboard)
        self.router.add_route('GET', '/api/status', self._handle_api_status)
        self.router.add_route('GET', '/api/sensors', self._handle_api_sensors)
        self.router.add_route('GET', '/api/sensors/{id}', self._handle_api_sensor)
        
        # Config routes
        self.router.add_route('GET', '/config', self._handle_config)
        self.router.add_route('GET', '/api/config', self._handle_api_config)
        self.router.add_route('POST', '/api/config', self._handle_api_config)
        self.router.add_route('GET', '/api/sensors/config', self._handle_api_sensors_config)
        self.router.add_route('POST', '/api/sensors/config', self._handle_api_sensors_config)
        self.router.add_route('POST', '/api/sensors', self._handle_api_add_sensor)
        self.router.add_route('DELETE', '/api/sensors/{id}', self._handle_api_remove_sensor)
        
        # Static files
        self.router.add_route('GET', '/css/{file}', self._handle_static_file)
        self.router.add_route('GET', '/js/{file}', self._handle_static_file)
        self.router.add_route('GET', '/images/{file}', self._handle_static_file)
        
        # CORS preflight
        self.router.add_route('OPTIONS', '/api/*', self._handle_cors_preflight)
        
        print("[APP] ✅ Rotas configuradas")
    
    def _handle_dashboard(self, request):
        """Handler para dashboard"""
        return dashboard_controller.handle_dashboard_request(request)
    
    def _handle_config(self, request):
        """Handler para configuração"""
        return config_controller.handle_config_request(request)
    
    def _handle_api_status(self, request):
        """Handler para API de status"""
        return dashboard_controller.handle_dashboard_request(request)
    
    def _handle_api_sensors(self, request):
        """Handler para API de sensores"""
        return dashboard_controller.handle_dashboard_request(request)
    
    def _handle_api_sensor(self, request):
        """Handler para API de sensor específico"""
        return dashboard_controller.handle_dashboard_request(request)
    
    def _handle_api_config(self, request):
        """Handler para API de configuração"""
        return config_controller.handle_config_request(request)
    
    def _handle_api_sensors_config(self, request):
        """Handler para API de configuração de sensores"""
        return config_controller.handle_config_request(request)
    
    def _handle_api_add_sensor(self, request):
        """Handler para adicionar sensor"""
        return config_controller.handle_config_request(request)
    
    def _handle_api_remove_sensor(self, request):
        """Handler para remover sensor"""
        return config_controller.handle_config_request(request)
    
    def _handle_static_file(self, request):
        """Handler para arquivos estáticos"""
        return dashboard_controller.handle_dashboard_request(request)
    
    def _handle_cors_preflight(self, request):
        """Handler para CORS preflight"""
        from core.response import cors_preflight_response
        return cors_preflight_response()
    
    def start(self, mode='STA'):
        """Inicia a aplicação"""
        if not self.initialize(mode):
            return False
        
        # Iniciar servidor HTTP
        if not self.http_server.start():
            return False
        
        self.running = True
        print("[APP] 🚀 Aplicação iniciada!")
        
        # Mostrar IP baseado no modo
        if mode == 'AP':
            print(f"[APP] 🌐 http://192.168.4.1:8080")
        else:
            print(f"[APP] 🌐 http://[IP_DO_ESP32]:8080")
        
        print("=" * 50)
        
        # Loop principal
        self._main_loop()
        
        return True
    
    def _main_loop(self):
        """Loop principal da aplicação"""
        while self.running:
            try:
                # Aceitar conexão
                client_socket, client_addr = self.http_server.socket.accept()
                
                # Processar requisição
                self._process_request(client_socket, client_addr)
                
                # Alimentar watchdog
                if self.wdt:
                    self.wdt.feed()
                
                # Otimização de memória
                gc.collect()
                
            except Exception as e:
                print(f"[APP] ❌ Erro no loop principal: {e}")
                time.sleep(0.1)
    
    def _process_request(self, client_socket, client_addr):
        """Processa requisição HTTP"""
        try:
            # Receber dados
            request_data = client_socket.recv(1024).decode('utf-8')
            if not request_data:
                return
            
            # Parse da requisição
            request_lines = request_data.split('\r\n')
            if not request_lines:
                return
            
            # Primeira linha: METHOD /path HTTP/1.1
            request_line = request_lines[0]
            parts = request_line.split(' ')
            
            if len(parts) < 2:
                return
            
            method = parts[0]
            path = parts[1]
            
            print(f"[APP] {method} {path} de {client_addr[0]}")
            
            # Criar contexto da requisição
            request = {
                'method': method,
                'path': path,
                'data': request_data,
                'params': {},
                'headers': self._parse_headers(request_data)
            }
            
            # Processar através do router
            response = self.router.process_request(method, path, request_data)
            
            # Enviar resposta
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"[APP] ❌ Erro ao processar requisição: {e}")
            try:
                error_response = error_response("Server Error")
                client_socket.send(error_response.encode('utf-8'))
            except:
                pass
        finally:
            client_socket.close()
    
    def _parse_headers(self, request_data):
        """Extrai headers da requisição"""
        headers = {}
        if not request_data:
            return headers
        
        lines = request_data.split('\r\n')
        for line in lines[1:]:  # Pular primeira linha
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        return headers
    
    def stop(self):
        """Para a aplicação"""
        self.running = False
        if self.http_server:
            self.http_server.stop()
        print("[APP] 🔴 Aplicação parada")
    
    def get_stats(self):
        """Retorna estatísticas da aplicação"""
        return {
            'app_version': '4.0.0',
            'running': self.running,
            'http_server_stats': self.http_server.get_stats() if self.http_server else None,
            'router_stats': self.router.get_routes_info() if self.router else None,
            'system_monitor_stats': system_monitor.get_stats(),
            'data_store_stats': data_store.get_cache_stats()
        }

def detect_mode():
    """Detecta se está em modo AP ou STA"""
    import network
    
    # Verificar se AP está ativo
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        return 'AP'
    
    # Verificar se STA está conectado
    sta = network.WLAN(network.STA_IF)
    if sta.active() and sta.isconnected():
        return 'STA'
    
    # Default para AP se não conseguir detectar
    return 'AP'

def main():
    """Função principal"""
    print("=" * 50)
    print("🔥 MONITOR MINER v4.0 - ARQUITETURA MODULAR")
    print("=" * 50)
    
    # Detectar modo
    mode = detect_mode()
    print(f"[APP] Modo detectado: {mode}")
    
    # Criar e iniciar aplicação
    app = MonitorMinerApp()
    
    try:
        app.start(mode)
    except KeyboardInterrupt:
        print("\n[APP] ⏹️ Interrompido pelo usuário")
    except Exception as e:
        print(f"[APP] ❌ Erro fatal: {e}")
    finally:
        app.stop()

if __name__ == "__main__":
    main()
