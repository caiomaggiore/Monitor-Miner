"""
Dashboard - Monitor Miner v3.0
SERVIDOR DASHBOARD: Apenas para página index.html
"""

import json
import network
import socket
import time
import select
import gc
from machine import WDT

# ============================================================================
# CONFIGURAÇÃO INICIAL
# ============================================================================

# NOTA: Este arquivo agora funciona como MÓDULO (importado pelo main.py)
# O servidor HTTP é gerenciado pelo main.py

# Configurar WiFi (apenas para obter IP)
sta = network.WLAN(network.STA_IF)
ip = sta.ifconfig()[0]

print("[DASH] ✅ Dashboard module carregado")

# Socket e Watchdog são gerenciados pelo main.py
# (Comentado para evitar conflito EADDRINUSE)
# s = socket.socket(...)
# wdt = WDT(...)

# ============================================================================
# IMPORTAÇÕES COM FALLBACK
# ============================================================================

# System Monitor com fallback
try:
    from system_monitor_simple import get_system_info
    print("[DASH] ✅ System Monitor carregado")
except Exception as e:
    print(f"[DASH] ⚠️ Erro ao carregar system_monitor: {e}")
    def get_system_info():
        return {
            'version': '3.2.2',
            'cpu_percent': 0.0,
            'memory_free': gc.mem_free(),
            'memory_total': gc.mem_free() + gc.mem_alloc(),
            'uptime': time.ticks_ms() // 1000
        }

# Memory Optimizer com fallback
try:
    from memory_optimizer import optimize_memory, cache_file, get_cached_file, clear_file_cache
    print("[DASH] ✅ Memory Optimizer carregado")
except Exception as e:
    print(f"[DASH] ⚠️ Erro ao carregar memory_optimizer: {e}")
    def optimize_memory():
        gc.collect()
        return 0
    def cache_file(filename, content):
        pass
    def get_cached_file(filename):
        return None
    def clear_file_cache():
        pass

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def load_file(filename):
    """Carrega arquivo com cache inteligente"""
    try:
        # Verificar cache primeiro
        cached = get_cached_file(filename)
        if cached:
            print(f"[DASH] Arquivo {filename} em cache ({len(cached)} bytes)")
            return cached
        
        # Carregar do disco
        with open(filename, 'r') as f:
            content = f.read()
            
        # Cache se não for muito grande
        if len(content) < 8192:  # 8KB
            cache_file(filename, content)
            print(f"[DASH] Cache: {filename} ({len(content)}B) - Total: {len(content)}B")
        else:
            print(f"[DASH] Arquivo {filename} muito grande, sem cache ({len(content)} bytes)")
            
        return content
    except Exception as e:
        print(f"[DASH] Erro ao carregar {filename}: {e}")
        return f"<h1>Erro ao carregar {filename}</h1>"

def load_sensors():
    """Carrega dados dos sensores"""
    try:
        with open('data/sensors.json', 'r') as f:
            return json.load(f)
    except:
        return {
            'temperature': 25.0,
            'humidity': 60.0,
            'miners': {'total': 0, 'online': 0, 'offline': 0},
            'power': {'consumption': 0.0, 'status': 'Desconhecido'}
        }

def http_response(content, content_type='text/html', status='200 OK'):
    """Cria resposta HTTP"""
    response = f"HTTP/1.1 {status}\r\n"
    response += f"Content-Type: {content_type}; charset=utf-8\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += content
    return response

# ============================================================================
# ARQUITETURA MODULAR - FUNÇÕES POR MÓDULO
# ============================================================================

def handle_dashboard_request(path, method, request_data):
    """Processa requisições do módulo Dashboard"""
    print(f"[DASH] Processando requisição Dashboard: {path}")
    
    if path == '/' or path == '/index.html':
        # Página Principal
        html = load_file('web/index.html')
        return http_response(html, 'text/html')
    elif path == '/api/sensors':
        # API Sensores
        sensors = load_sensors()
        data = json.dumps({
            'success': True,
            'data': sensors
        })
        return http_response(data, 'application/json')
    elif path == '/api/status':
        # API Status do Sistema
        try:
            system_info = get_system_info()
            system_info['ip'] = ip
            system_info['network'] = {'ip': ip, 'connected': True}
            
            print(f"[DASH] Enviando status: IP={ip}, uptime={time.ticks_ms() // 1000}")
            
            data = json.dumps({
                'success': True,
                'data': system_info
            })
            return http_response(data, 'application/json')
            
        except Exception as e:
            print(f"[DASH] Erro no system_monitor: {e}")
            data = json.dumps({
                'success': True,
                'data': {
                    'version': '3.2.2',
                    'mode': 'DASHBOARD',
                    'memory_free': gc.mem_free(),
                    'memory_total': gc.mem_free() + gc.mem_alloc(),
                    'cpu_percent': 0.0,
                    'ip': ip,
                    'uptime': time.ticks_ms() // 1000,
                    'error': str(e),
                    'fallback': True
                }
            })
            return http_response(data, 'application/json')
    else:
        return None

def handle_assets_request(path, method, request_data):
    """Processa requisições de assets (CSS, JS, etc.)"""
    print(f"[ASSETS] Processando requisição Asset: {path}")
    
    if path.startswith('/css/'):
        # CSS
        filename = f"web{path}"
        content = load_file(filename)
        return http_response(content, 'text/css')
    elif path.startswith('/js/'):
        # JavaScript
        filename = f"web{path}"
        content = load_file(filename)
        return http_response(content, 'application/javascript')
    elif path.startswith('/assets/'):
        # Outros assets
        filename = f"web{path}"
        content = load_file(filename)
        return http_response(content, 'application/octet-stream')
    else:
        return None

# ============================================================================
# FUNÇÃO DE HANDLER PARA ROTEADOR
# ============================================================================

def handle_request(conn, method, path, request_data):
    """Handler para requisições do dashboard"""
    print(f"[DASH] Processando: {method} {path}")
    
    try:
        # Tentar processar com módulo Dashboard
        response = handle_dashboard_request(path, method, request_data)
        
        # Se não processado, tentar módulo Assets
        if response is None:
            response = handle_assets_request(path, method, request_data)
        
        # Se nenhum módulo processou, retornar 404
        if response is None:
            print(f"[DASH] 404 - Rota não encontrada: {path}")
            response = http_response("<h1>404 Not Found</h1>", status='404 Not Found')
        
        # Enviar resposta em chunks para economizar memória
        chunk_size = 512
        
        try:
            response_bytes = response.encode('utf-8')
            for i in range(0, len(response_bytes), chunk_size):
                chunk = response_bytes[i:i + chunk_size]
                sent = conn.send(chunk)
                if sent == 0:
                    break
                time.sleep(0.01)  # Pequena pausa entre chunks
                    
            print(f"[DASH] Resposta enviada: {len(response_bytes)} bytes")
        except Exception as e:
            print(f"[DASH] Erro ao enviar resposta: {e}")
        finally:
            conn.close()
            gc.collect()
        
    except Exception as e:
        print(f"[DASH] Erro ao processar requisição: {e}")
        try:
            conn.close()
        except:
            pass
        gc.collect()

# ============================================================================
# LOOP PRINCIPAL (DESABILITADO - main.py gerencia o loop)
# ============================================================================

# NOTA: O loop abaixo está comentado porque o dashboard.py agora funciona como
# módulo importado pelo main.py. O loop principal está no main.py.

# Para executar dashboard.py standalone (debug), descomente o código abaixo:

"""
# Contador para tasks periódicas
last_sensor_update = time.ticks_ms()
sensor_interval = 10000  # 10 segundos

# Recriar socket e watchdog para modo standalone
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(False)
s.bind((ip, 8080))
s.listen(5)
wdt = WDT(timeout=15000)

# Loop principal com select()
print("[DASH] 🚀 Iniciando loop principal...")
loop_count = 0

while True:
    loop_count += 1
    
    # Feed watchdog a cada iteração (previne reset)
    wdt.feed()
    
    # Log a cada 1000 iterações (100 segundos) - menos spam
    if loop_count % 1000 == 0:
        print(f"[DASH] Sistema ativo: {loop_count} iterações")
    
    try:
        # select() espera conexão ou timeout (50ms) - mais rápido
        readable, _, _ = select.select([s], [], [], 0.05)
        
        if not readable:
            # Sem conexão - executar tasks periódicas
            current_time = time.ticks_ms()
            
            # Atualizar sensores a cada 10s
            if time.ticks_diff(current_time, last_sensor_update) > sensor_interval:
                # TODO: Implementar leitura real de sensores
                # sensors_data = read_all_sensors()
                # save_sensors(sensors_data)
                last_sensor_update = current_time
                # print("[DASH] Sensores atualizados")
            
            continue
        
        # Tem conexão pronta!
        conn, client_addr = s.accept()
        print(f"[DASH] Conexão de {client_addr}")
        
        # Feed watchdog antes de processar conexão
        wdt.feed()
        
        try:
            # Receber requisição
            request_data = conn.recv(1024).decode('utf-8')
            if not request_data:
                conn.close()
                continue
            
            # Parse da requisição
            lines = request_data.split('\n')
            if not lines:
                conn.close()
                continue
                    
            request_line = lines[0]
            parts = request_line.split()
            if len(parts) < 2:
                conn.close()
                continue
        
            method = parts[0]
            path = parts[1]
            
            print(f"[DASH] {method} {path}")
            
            # ============================================================================
            # ROTEAMENTO MODULAR - ARQUITETURA SEPARADA POR MÓDULOS
            # ============================================================================
            
            # DASHBOARD APENAS PARA INDEX - ARQUITETURA MODULAR
            # Tentar processar com módulo Dashboard
            response = handle_dashboard_request(path, method, request_data)
            
            # Se não processado, tentar módulo Assets
            if response is None:
                response = handle_assets_request(path, method, request_data)
            
            # Se nenhum módulo processou, retornar 404
            if response is None:
                print(f"[DASH] 404 - Rota não encontrada: {path}")
                response = http_response("<h1>404 Not Found</h1>", status='404 Not Found')
            
            # Feed watchdog antes de enviar resposta
            wdt.feed()
            
            # Enviar resposta em chunks para economizar memória
            chunk_size = 512
            
            try:
                response_bytes = response.encode('utf-8')
                for i in range(0, len(response_bytes), chunk_size):
                    chunk = response_bytes[i:i + chunk_size]
                    sent = conn.send(chunk)
                    if sent == 0:
                        break
                    time.sleep(0.01)  # Pequena pausa entre chunks
                    
                    # Feed watchdog a cada 4 chunks (2KB) para respostas grandes
                    if i > 0 and i % (chunk_size * 4) == 0:
                        wdt.feed()
                        
                print(f"[DASH] Resposta enviada: {len(response_bytes)} bytes")
            except Exception as e:
                print(f"[DASH] Erro ao enviar resposta: {e}")
            finally:
                conn.close()
                gc.collect()
            
            # Otimização de memória e limpeza periódica
            if time.ticks_ms() % 60000 < 100:  # A cada ~1 minuto
                clear_file_cache()
                freed = optimize_memory()  # Otimizar memória
                if freed > 0:
                    print(f"[DASH] Memória otimizada: {freed}KB liberados")
            
            # Feed do watchdog ANTES de processar requisições grandes
            if 'config.html' in path:
                wdt.feed()
                print(f"[DASH] Watchdog alimentado para config.html")
        
        except Exception as e:
            print(f"[DASH] Erro ao processar conexão: {e}")
            try:
                conn.close()
            except:
                pass
            gc.collect()
    
    except Exception as e:
        print(f"[DASH] ❌ Erro no loop principal: {e}")
        gc.collect()  # Limpar memória em caso de erro
        time.sleep(0.1)  # Pequena pausa antes de continuar
"""

# Fim do modo standalone (comentado)
print("[DASH] ✅ Módulo dashboard.py pronto para uso pelo main.py")
