"""
Dashboard - Monitor Miner v3.0
Modo STA: Servidor Síncrono (socket puro)
MOTIVO: Microdot + asyncio causa crash também em modo STA
"""

import socket
import network
import json
import time
import gc
import select

print("[DASH] ========================================")
print("[DASH] Dashboard - Servidor Síncrono")
print("[DASH] ========================================")

gc.collect()
print(f"[DASH] Memória: {gc.mem_free() / 1024:.1f}KB")

# ============================================================================
# FUNÇÕES
# ============================================================================

def load_sensors():
    """Carrega dados dos sensores"""
    try:
        with open('data/sensors.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "temperature": 0.0,
            "humidity": 0.0,
            "miners": {"total": 0, "online": 0, "offline": 0},
            "power": {"consumption": 0.0, "status": "unknown"},
            "last_update": 0
        }

def load_file(filename):
    """Carrega arquivo"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"[DASH] Erro ao carregar {filename}: {e}")
        return "<html><body><h1>Erro</h1></body></html>"

def http_response(content, content_type='text/html', status='200 OK'):
    """Resposta HTTP com CORS"""
    response = f"HTTP/1.1 {status}\r\n"
    response += f"Content-Type: {content_type}; charset=utf-8\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += "Access-Control-Allow-Origin: *\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    
    if isinstance(content, str):
        return response.encode('utf-8') + content.encode('utf-8')
    else:
        return response.encode('utf-8') + content

def parse_request(request_data):
    """Parse requisição"""
    try:
        request_str = request_data.decode('utf-8')
        first_line = request_str.split('\r\n')[0]
        method, path = first_line.split(' ')[0:2]
        return method, path
    except:
        return 'GET', '/'

# ============================================================================
# SERVIDOR
# ============================================================================

# Obter IP
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    print("[DASH] ⚠️ WiFi desconectado! Reiniciando...")
    import machine
    time.sleep(2)
    machine.reset()

ip = wlan.ifconfig()[0]
port = 8080
addr = (ip, port)

# Configurar socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(False)  # Non-blocking para usar select()
s.bind(addr)
s.listen(5)

print("=" * 40)
print(f"[DASH] ✅ Servidor rodando!")
print(f"[DASH] ✅ Modo: Pseudo-assíncrono (select)")
print("=" * 40)
print(f"[DASH] 🌐 http://{ip}:{port}")
print("=" * 40)

# Contador para tasks periódicas
last_sensor_update = time.ticks_ms()
sensor_interval = 10000  # 10 segundos

# Loop principal com select()
while True:
    try:
        # select() espera conexão ou timeout (100ms)
        readable, _, _ = select.select([s], [], [], 0.1)
        
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
        
        conn.settimeout(5.0)
        request_data = conn.recv(2048)
        
        if not request_data:
            conn.close()
            continue
        
        method, path = parse_request(request_data)
        print(f"[DASH] {method} {path}")
        
        # Roteamento
        if path == '/' or path.startswith('/index'):
            # Dashboard
            html = load_file('web/index.html')
            response = http_response(html, 'text/html')
            
        elif '/css/style.css' in path:
            # CSS
            print(f"[DASH] Servindo style.css")
            css = load_file('web/css/style.css')
            response = http_response(css, 'text/css')
            
        elif '/js/dashboard.js' in path:
            # JavaScript
            print(f"[DASH] Servindo dashboard.js")
            js = load_file('web/js/dashboard.js')
            response = http_response(js, 'application/javascript')
            
        elif path.startswith('/api/sensors'):
            # API Sensores
            data = json.dumps({
                'success': True,
                'data': load_sensors()
            })
            response = http_response(data, 'application/json')
            
        elif path.startswith('/api/status'):
            # API Status
            data = json.dumps({
                'success': True,
                'data': {
                    'version': '3.0',
                    'mode': 'STA',
                    'memory_free': gc.mem_free(),
                    'ip': ip,
                    'uptime': time.ticks_ms() // 1000
                }
            })
            response = http_response(data, 'application/json')
            
        else:
            # 404
            data = json.dumps({'error': '404'})
            response = http_response(data, 'application/json', '404 Not Found')
        
        conn.send(response)
        conn.close()
        gc.collect()
        
    except Exception as e:
        print(f"[DASH] Erro: {e}")
        try:
            conn.close()
        except:
            pass
        gc.collect()
