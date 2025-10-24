"""
Setup - Monitor Miner v3.2.1
Modo AP: Configuração WiFi com Site Survey
Servidor HTTP Síncrono (socket puro)
WATCHDOG: Implementado para garantir recuperação em caso de travamento
"""

import socket
import network
import json
import time
import gc
import machine
import select
from machine import WDT

print("[SETUP] ========================================")
print("[SETUP] Modo Setup - Configuração WiFi")
print("[SETUP] ========================================")

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def load_config():
    """Carrega configuração"""
    try:
        with open('data/config.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "wifi": {"ssid": "", "password": "", "configured": False},
            "system": {"name": "Monitor Miner", "version": "3.0", "first_boot": True}
        }

def save_config(config):
    """Salva configuração"""
    try:
        with open('data/config.json', 'w') as f:
            json.dump(config, f)
        return True
    except Exception as e:
        print(f"[SETUP] Erro ao salvar: {e}")
        return False

def load_file(filename):
    """Carrega arquivo HTML"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"[SETUP] Erro ao carregar {filename}: {e}")
        return "<html><body><h1>Erro ao carregar página</h1></body></html>"

def scan_networks():
    """Escaneia redes WiFi"""
    start_time = time.ticks_ms()
    print("[SETUP] Escaneando redes...")
    
    sta = network.WLAN(network.STA_IF)
    was_active = sta.active()
    
    if not was_active:
        print("[SETUP]   Ativando STA...")
        sta.active(True)
        time.sleep(1)
    
    print("[SETUP]   Iniciando scan...")
    networks_raw = sta.scan()
    print(f"[SETUP]   Scan concluído ({len(networks_raw)} redes brutas)")
    
    if not was_active:
        sta.active(False)
    
    # Formatar
    networks = []
    seen = set()
    
    for net in networks_raw:
        ssid = net[0].decode('utf-8')
        if not ssid or ssid in seen:
            continue
        seen.add(ssid)
        
        auth = net[4]
        security = {0: "Open", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}.get(auth, "WPA2")
        
        networks.append({
            'ssid': ssid,
            'rssi': net[3],
            'channel': net[2],
            'security': security
        })
    
    elapsed = time.ticks_diff(time.ticks_ms(), start_time)
    print(f"[SETUP] ✅ Encontradas {len(networks)} redes ({elapsed}ms)")
    return networks

def connect_wifi(ssid, password):
    """Conecta ao WiFi"""
    print(f"[SETUP] Conectando a: {ssid}")
    
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    time.sleep(1)
    
    sta.connect(ssid, password)
    
    timeout = 15
    while timeout > 0 and not sta.isconnected():
        time.sleep(1)
        timeout -= 1
    
    if sta.isconnected():
        ip = sta.ifconfig()[0]
        print(f"[SETUP] ✅ Conectado! IP: {ip}")
        
        # Salvar config
        config = load_config()
        config['wifi']['ssid'] = ssid
        config['wifi']['password'] = password
        config['wifi']['configured'] = True
        config['system']['first_boot'] = False
        save_config(config)
        
        return True, ip
    else:
        print("[SETUP] ❌ Falha na conexão")
        sta.active(False)
        return False, None

def http_response(content, content_type='text/html', status='200 OK'):
    """Cria resposta HTTP com CORS"""
    response = f"HTTP/1.1 {status}\r\n"
    response += f"Content-Type: {content_type}; charset=utf-8\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += "Access-Control-Allow-Origin: *\r\n"
    response += "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
    response += "Access-Control-Allow-Headers: Content-Type\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    
    if isinstance(content, str):
        return response.encode('utf-8') + content.encode('utf-8')
    else:
        return response.encode('utf-8') + content

def send_response_safe(conn, response):
    """Envia resposta por chunks e aguarda confirmação"""
    try:
        # Enviar por chunks pequenos (512 bytes) para garantir entrega
        chunk_size = 512
        total_sent = 0
        
        while total_sent < len(response):
            chunk = response[total_sent:total_sent + chunk_size]
            sent = conn.send(chunk)
            if sent == 0:
                print(f"[SETUP_WIFI] Erro: Conexão fechada pelo cliente")
                return False
            total_sent += sent
            
            # Aguardar um pouco para garantir entrega
            time.sleep(0.01)  # 10ms entre chunks
            
        print(f"[SETUP_WIFI] Resposta enviada: {total_sent}/{len(response)} bytes")
        
        # AGUARDAR CONFIRMAÇÃO: Tentar receber dados do cliente
        # (isso força o cliente a processar completamente antes de fechar)
        try:
            conn.settimeout(1.0)  # 1 segundo para confirmação
            confirmation = conn.recv(1)  # Tentar receber 1 byte
            print(f"[SETUP_WIFI] Confirmação recebida: {len(confirmation) if confirmation else 0} bytes")
        except:
            # Timeout é normal - cliente não enviou confirmação
            print(f"[SETUP_WIFI] Cliente não confirmou (timeout normal)")
        
        return total_sent == len(response)
        
    except Exception as e:
        print(f"[SETUP_WIFI] Erro ao enviar: {e}")
        return False

def parse_request(request_data):
    """Parse básico da requisição HTTP"""
    try:
        # Decodificar uma vez
        request_str = request_data.decode('utf-8')
        
        # Separar headers e body
        parts = request_str.split('\r\n\r\n', 1)
        headers_part = parts[0]
        body_part = parts[1] if len(parts) > 1 else ''
        
        # Parse primeira linha
        first_line = headers_part.split('\r\n')[0]
        method, path = first_line.split(' ')[0:2]
        
        # Parse body (JSON)
        body = None
        if body_part.strip():
            print(f"[PARSE] Body raw: {body_part[:100]}")  # Debug
            try:
                body = json.loads(body_part)
                print(f"[PARSE] Body parsed: {body}")  # Debug
            except Exception as e:
                print(f"[PARSE] Erro ao parsear JSON: {e}")
                print(f"[PARSE] Body era: {body_part}")
        
        return method, path, body
    except Exception as e:
        print(f"[PARSE] Erro geral: {e}")
        return 'GET', '/', None

# ============================================================================
# SERVIDOR HTTP SÍNCRONO
# ============================================================================

def run_server():
    """Servidor HTTP com select() - pseudo-assíncrono"""
    
    # Configurar socket
    addr = ('192.168.4.1', 8080)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(True)   # Blocking para setup síncrono!
    s.bind(addr)
    s.listen(5)
    
    print("[SETUP] ========================================")
    print(f"[SETUP_WIFI] ✅ Servidor rodando em http://{addr[0]}:{addr[1]}")
    print("[SETUP_WIFI] ✅ Modo: Síncrono (1 usuário)")
    print("[SETUP_WIFI] ========================================")
    
    # ============================================================================
    # WATCHDOG TIMER - Recuperação automática em caso de travamento
    # ============================================================================
    print("[SETUP_WIFI] Inicializando Watchdog Timer (10s)...")
    wdt = WDT(timeout=10000)  # 10 segundos - reinicia se não receber feed()
    print("[SETUP_WIFI] ✅ Watchdog ativo - Sistema protegido contra travamentos")
    
    # Loop principal SÍNCRONO
    while True:
        # Feed watchdog a cada iteração (previne reset)
        wdt.feed()
        try:
            # SÍNCRONO: Aguarda conexão (sem timeout)
            print(f"[SETUP_WIFI] Aguardando conexão...")
            conn, client_addr = s.accept()
            print(f"[SETUP_WIFI] ============ Nova Conexão ============")
            print(f"[SETUP_WIFI] Cliente: {client_addr}")
            
            # Receber requisição
            conn.settimeout(5.0)
            request_data = conn.recv(2048)
            
            if not request_data:
                print(f"[SETUP] ⚠️ Requisição vazia")
                conn.close()
                continue
            
            # Parse
            method, path, body = parse_request(request_data)
            print(f"[SETUP] → {method} {path}")
            if body:
                print(f"[SETUP] Body: {body}")
            
            # Roteamento
            if method == 'OPTIONS':
                # Preflight CORS
                print(f"[SETUP] Preflight CORS para {path}")
                response = http_response('', 'text/plain')
                
            elif path == '/' or path.startswith('/index') or path.startswith('/setup_wifi.html'):
                # Página principal (setup_wifi.html)
                print(f"[SETUP_WIFI] Servindo setup_wifi.html")
                html = load_file('web/setup_wifi.html')
                response = http_response(html, 'text/html')
                
            elif '/css/base.css' in path:
                # CSS Base
                print(f"[SETUP_WIFI] Servindo base.css")
                css = load_file('web/css/base.css')
                print(f"[SETUP_WIFI] CSS carregado: {len(css)} bytes")
                response = http_response(css, 'text/css')
                
            elif '/css/style.css' in path or '/css/style.min.css' in path:
                # CSS Legacy (compatibilidade)
                print(f"[SETUP_WIFI] Servindo style.min.css (legacy)")
                css = load_file('web/css/style.min.css')
                print(f"[SETUP_WIFI] CSS carregado: {len(css)} bytes")
                response = http_response(css, 'text/css')
                
            elif '/js/setup_wifi.js' in path:
                # JavaScript
                print(f"[SETUP_WIFI] Servindo setup_wifi.js")
                js = load_file('web/js/setup_wifi.js')
                print(f"[SETUP_WIFI] JS carregado: {len(js)} bytes")
                response = http_response(js, 'application/javascript')
                
            elif path == '/api/scan' or path.startswith('/api/scan'):
                # API Scan
                print(f"[SETUP] Executando scan de redes...")
                networks = scan_networks()
                print(f"[SETUP] Scan retornou {len(networks)} redes")
                
                response_data = json.dumps({
                    'success': True,
                    'networks': networks,
                    'count': len(networks)
                })
                print(f"[SETUP] Enviando resposta: {len(response_data)} bytes")
                response = http_response(response_data, 'application/json')
                
            elif path == '/api/connect' and method == 'POST':
                # API Connect
                if body:
                    ssid = body.get('ssid', '')
                    password = body.get('password', '')
                    
                    success, ip = connect_wifi(ssid, password)
                    
                    if success:
                        response_data = json.dumps({
                            'success': True,
                            'ip': ip,
                            'message': 'Conectado! Reiniciando...'
                        })
                        response = http_response(response_data, 'application/json')
                        
                        # Enviar resposta e reiniciar
                        send_response_safe(conn, response)
                        time.sleep(0.5)  # Aguardar processamento
                        conn.close()
                        
                        print("[SETUP] ========================================")
                        print("[SETUP] ✅ WiFi configurado! Reiniciando...")
                        print("[SETUP] ========================================")
                        
                        time.sleep(2)
                        machine.reset()
                    else:
                        response_data = json.dumps({
                            'success': False,
                            'error': 'Falha na conexão. Verifique a senha.'
                        })
                        response = http_response(response_data, 'application/json')
                else:
                    response_data = json.dumps({'success': False, 'error': 'Dados inválidos'})
                    response = http_response(response_data, 'application/json')
                    
            elif path == '/api/status':
                # API Status
                response_data = json.dumps({
                    'success': True,
                    'data': {
                        'version': '3.0',
                        'mode': 'AP',
                        'memory_free': gc.mem_free(),
                        'ip': '192.168.4.1'
                    }
                })
                response = http_response(response_data, 'application/json')
                
            else:
                # 404
                response_data = json.dumps({'error': '404 - Not Found'})
                response = http_response(response_data, 'application/json', '404 Not Found')
            
            # Enviar resposta
            print(f"[SETUP_WIFI] Enviando resposta ({len(response)} bytes)...")
            success = send_response_safe(conn, response)
            if success:
                print(f"[SETUP_WIFI] ✅ Resposta enviada completamente")
            else:
                print(f"[SETUP_WIFI] ❌ Erro no envio da resposta")
            
            # AGUARDAR antes de fechar (garantir que cliente processou)
            print(f"[SETUP_WIFI] Aguardando processamento do cliente...")
            time.sleep(0.5)  # 500ms para garantir processamento
            
            conn.close()
            print(f"[SETUP_WIFI] ============ Conexão Fechada ============")
            
            # Limpar memória
            gc.collect()
            
        except Exception as e:
            print(f"[SETUP] Erro: {e}")
            try:
                conn.close()
            except:
                pass
            gc.collect()

# ============================================================================
# INICIAR AUTOMATICAMENTE
# ============================================================================

# Garantir que AP está ativo
ap = network.WLAN(network.AP_IF)
if not ap.active():
    print("[SETUP] Ativando AP...")
    ap.active(True)
    time.sleep(1)

# Executar servidor (bloqueante - isso impede que main.py seja carregado)
try:
    run_server()
except KeyboardInterrupt:
    print("[SETUP] Servidor encerrado")
except Exception as e:
    print(f"[SETUP] Erro fatal: {e}")

