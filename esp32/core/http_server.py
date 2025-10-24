# ============================================================================
# HTTP SERVER BASE - Monitor Miner v4.0
# ============================================================================
# Servidor HTTP unificado e otimizado para ESP32
# - Gerenciamento de conexões
# - Watchdog integrado
# - Otimização de memória
# - Cache de arquivos estáticos
# ============================================================================

import socket
import gc
import time
from machine import WDT

class HTTPServer:
    """
    Servidor HTTP base para ESP32
    - Gerenciamento unificado de conexões
    - Watchdog integrado
    - Otimização de memória
    """
    
    def __init__(self, host='0.0.0.0', port=8080, max_connections=5):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.socket = None
        self.wdt = None
        self.running = False
        
        # Cache de arquivos estáticos
        self.file_cache = {}
        self.cache_max_size = 5  # Máximo 5 arquivos em cache
        
        print(f"[HTTP] Inicializando servidor HTTP {host}:{port}")
    
    def start(self):
        """Inicia o servidor HTTP"""
        try:
            # Criar socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.max_connections)
            
            # Inicializar watchdog
            self.wdt = WDT(timeout=15)  # 15 segundos
            
            self.running = True
            print(f"[HTTP] ✅ Servidor rodando em {self.host}:{self.port}")
            print(f"[HTTP] ✅ Watchdog ativo (15s)")
            
            return True
            
        except Exception as e:
            print(f"[HTTP] ❌ Erro ao iniciar servidor: {e}")
            return False
    
    def stop(self):
        """Para o servidor HTTP"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("[HTTP] 🔴 Servidor parado")
    
    def handle_request(self, client_socket, client_addr):
        """
        Processa uma requisição HTTP
        - Parse do request
        - Roteamento
        - Resposta
        """
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
            
            print(f"[HTTP] {method} {path} de {client_addr[0]}")
            
            # Roteamento será implementado pelo router
            # Por enquanto, resposta básica
            response = self._create_response("200 OK", "text/html", "Hello v4.0!")
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"[HTTP] ❌ Erro ao processar requisição: {e}")
            try:
                error_response = self._create_response("500 Internal Server Error", "text/plain", "Server Error")
                client_socket.send(error_response.encode('utf-8'))
            except:
                pass
        finally:
            client_socket.close()
    
    def _create_response(self, status, content_type, body):
        """Cria resposta HTTP"""
        response = f"HTTP/1.1 {status}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body
        return response
    
    def serve_file(self, file_path, content_type=None):
        """
        Serve arquivo estático com cache
        - Cache LRU para otimização
        - Detecção automática de content-type
        """
        try:
            # Verificar cache
            if file_path in self.file_cache:
                print(f"[HTTP] 📁 Cache hit: {file_path}")
                return self.file_cache[file_path]
            
            # Ler arquivo
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Detectar content-type se não especificado
            if not content_type:
                if file_path.endswith('.html'):
                    content_type = 'text/html'
                elif file_path.endswith('.css'):
                    content_type = 'text/css'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript'
                elif file_path.endswith('.json'):
                    content_type = 'application/json'
                else:
                    content_type = 'text/plain'
            
            # Criar resposta
            response = self._create_response("200 OK", content_type, content)
            
            # Adicionar ao cache (LRU)
            if len(self.file_cache) >= self.cache_max_size:
                # Remover item mais antigo
                oldest_key = next(iter(self.file_cache))
                del self.file_cache[oldest_key]
            
            self.file_cache[file_path] = response
            print(f"[HTTP] 📁 Cache miss: {file_path} ({len(content)} bytes)")
            
            return response
            
        except Exception as e:
            print(f"[HTTP] ❌ Erro ao servir arquivo {file_path}: {e}")
            return self._create_response("404 Not Found", "text/plain", "File not found")
    
    def run(self):
        """
        Loop principal do servidor
        - Aceita conexões
        - Processa requisições
        - Gerencia watchdog
        """
        if not self.running:
            print("[HTTP] ❌ Servidor não está rodando")
            return
        
        print("[HTTP] 🚀 Iniciando loop principal...")
        
        while self.running:
            try:
                # Aceitar conexão
                client_socket, client_addr = self.socket.accept()
                
                # Processar requisição
                self.handle_request(client_socket, client_addr)
                
                # Alimentar watchdog
                if self.wdt:
                    self.wdt.feed()
                
                # Garbage collection periódico
                gc.collect()
                
            except Exception as e:
                print(f"[HTTP] ❌ Erro no loop principal: {e}")
                time.sleep(0.1)
    
    def get_stats(self):
        """Retorna estatísticas do servidor"""
        return {
            'running': self.running,
            'cache_size': len(self.file_cache),
            'cache_files': list(self.file_cache.keys())
        }
