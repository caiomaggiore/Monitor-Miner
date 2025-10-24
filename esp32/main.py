"""
Main - Monitor Miner v3.0
ROTEADOR INTELIGENTE: Decide qual servidor carregar baseado na requisição
"""

import json
import network
import socket
import time
import select
from machine import WDT

print("[MAIN] ========================================")
print("[MAIN] Monitor Miner v3.0 - Roteador Inteligente")
print("[MAIN] ========================================")

# Verificar modo
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)

if ap.active():
    # Modo AP - Carregar setup_wifi
    print("[MAIN] Modo AP detectado → Carregando setup_wifi.py")
    import setup_wifi
    
elif sta.active() and sta.isconnected():
    # Modo STA - Roteador inteligente
    print("[MAIN] Modo STA detectado → Iniciando roteador inteligente")
    
    # Configurar WiFi
    ip = sta.ifconfig()[0]
    port = 8080
    addr = (ip, port)
    
    # Configurar socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(False)
    s.bind(addr)
    s.listen(5)
    
    print("=" * 40)
    print(f"[MAIN] ✅ Roteador rodando!")
    print(f"[MAIN] ✅ IP: {ip}:{port}")
    print("=" * 40)
    print(f"[MAIN] 🌐 http://{ip}:{port}")
    print("=" * 40)
    
    # Watchdog Timer
    print("[MAIN] Inicializando Watchdog Timer (15s)...")
    wdt = WDT(timeout=15000)
    print("[MAIN] ✅ Watchdog ativo")
    
    # Importar servidores
    import dashboard
    import config
    
    print("[MAIN] 🚀 Iniciando roteador...")
    
    while True:
        wdt.feed()
        
        try:
            # select() espera conexão ou timeout (50ms)
            readable, _, _ = select.select([s], [], [], 0.05)
            
            if not readable:
                continue
            
            # Tem conexão pronta!
            conn, client_addr = s.accept()
            print(f"[MAIN] Conexão de {client_addr}")
            
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
                
                print(f"[MAIN] {method} {path}")
                
                # ROTEAMENTO INTELIGENTE
                if path == '/config' or path.startswith('/config') or path.startswith('/api/sensors/config') or path.startswith('/api/sensors/add') or path.startswith('/api/sensors/remove'):
                    # Config - Redirecionar para servidor config
                    print("[MAIN] → Roteando para CONFIG")
                    config.handle_request(conn, method, path, request_data)
                else:
                    # Dashboard - Redirecionar para servidor dashboard
                    print("[MAIN] → Roteando para DASHBOARD")
                    dashboard.handle_request(conn, method, path, request_data)
                
            except Exception as e:
                print(f"[MAIN] Erro ao processar conexão: {e}")
                try:
                    conn.close()
                except:
                    pass
        
        except Exception as e:
            print(f"[MAIN] ❌ Erro no roteador: {e}")
            time.sleep(0.1)
    
else:
    print("[MAIN] ⚠️ Nenhuma interface ativa! Reiniciando...")
    import machine
    import time
    time.sleep(2)
    machine.reset()
