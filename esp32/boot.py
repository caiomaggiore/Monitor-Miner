"""
Boot - Monitor Miner v4.0
MINIMALISTA: Apenas verifica configuração e direciona

Fluxo:
1. Desliga interfaces
2. Verifica se WiFi está configurado
3. Se SIM → Tenta conectar → main.py (STA + v4.0)
4. Se NÃO ou FALHA → main.py (AP + v4.0)
"""

import network
import time
import gc
import json

# ============================================================================
# HELPERS
# ============================================================================

def format_mem(b):
    """Formata bytes para KB"""
    return f"{b/1024:.1f}KB ({b}b)"

def load_config():
    """Carrega configuração WiFi"""
    try:
        with open('data/config.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "wifi": {"ssid": "", "password": "", "configured": False},
            "system": {"name": "Monitor Miner", "version": "3.0", "first_boot": True}
        }

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

print("[BOOT] ========================================")
print("[BOOT] Monitor Miner v4.0 - Boot")
print("[BOOT] ========================================")

# [1] Desligar tudo
print("[BOOT] [1/4] Desligando interfaces...")
sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

if sta.active():
    sta.disconnect()
    sta.active(False)
    time.sleep(1)

if ap.active():
    ap.active(False)
    time.sleep(1)

print("[BOOT]   ✅ Interfaces desligadas")

# [2] Limpar memória
print("[BOOT] [2/4] Limpando memória...")
gc.collect()
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
print(f"[BOOT]   Memória: {format_mem(gc.mem_free())}")

# [3] Verificar configuração
print("[BOOT] [3/4] Verificando configuração...")
config = load_config()
wifi_configured = config.get('wifi', {}).get('configured', False)
ssid = config.get('wifi', {}).get('ssid', '')
password = config.get('wifi', {}).get('password', '')

print(f"[BOOT]   WiFi configurado: {wifi_configured}")

# [4] Decidir modo
print("[BOOT] [4/4] Decidindo modo...")

if wifi_configured and ssid:
    # Tentar conectar em modo STA
    print(f"[BOOT]   → Conectando a: {ssid}")
    
    sta.active(True)
    time.sleep(1)
    sta.connect(ssid, password)
    
    # Aguardar (15s)
    timeout = 15
    while timeout > 0 and not sta.isconnected():
        time.sleep(1)
        timeout -= 1
    
    if sta.isconnected():
        # ✅ SUCESSO - Modo STA
        ip = sta.ifconfig()[0]
        print("=" * 40)
        print("[BOOT] ✅ CONECTADO!")
        print("=" * 40)
        print(f"[BOOT] SSID: {ssid}")
        print(f"[BOOT] IP: {ip}")
        print(f"[BOOT] 🌐 http://{ip}:8080")
        print("=" * 40)
        print("[BOOT] ➡️  Carregando main.py (Dashboard)")
        print("=" * 40)
        
        gc.collect()
        
        # Importar main.py (modo STA)
        import main
        
    else:
        # ❌ FALHA - Entrar em modo AP
        print("[BOOT] ❌ Falha ao conectar")
        print("[BOOT] ➡️  Entrando em modo Setup...")
        
        sta.active(False)
        time.sleep(1)
        
        # Configurar AP
        ap.active(True)
        time.sleep(1)
        ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
        ap.config(essid='MonitorMiner_Setup', authmode=0)
        time.sleep(1)
        
        print("=" * 40)
        print("[BOOT] ✅ AP ATIVO")
        print("=" * 40)
        print("[BOOT] WiFi: MonitorMiner_Setup")
        print("[BOOT] 🌐 http://192.168.4.1:8080")
        print("=" * 40)
        print("[BOOT] ➡️  Carregando setup_wifi.py (Site Survey)")
        print("=" * 40)
        
        gc.collect()
        
        # Importar setup_wifi.py (modo AP)
        import setup_wifi

else:
    # Não configurado - Modo AP
    print("[BOOT]   → Não configurado")
    
    # Configurar AP
    ap.active(True)
    time.sleep(1)
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    ap.config(essid='MonitorMiner_Setup', authmode=0)
    time.sleep(1)
    
    print("=" * 40)
    print("[BOOT] ✅ AP ATIVO")
    print("=" * 40)
    print("[BOOT] WiFi: MonitorMiner_Setup")
    print("[BOOT] 🌐 http://192.168.4.1:8080")
    print("=" * 40)
    print("[BOOT] ➡️  Carregando main.py v4.0 (Modo AP)")
    print("=" * 40)
    
    gc.collect()
    
    # Importar main.py v4.0 (modo AP)
    import main
