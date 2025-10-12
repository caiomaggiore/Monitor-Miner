"""
Main - Monitor Miner v3.0
ROTEADOR: Decide se carrega setup.py ou dashboard.py
"""

import json
import network

print("[MAIN] ========================================")
print("[MAIN] Monitor Miner v3.0")
print("[MAIN] ========================================")

# Verificar modo
ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)

if ap.active():
    # Modo AP - Carregar setup_wifi
    print("[MAIN] Modo AP detectado → Carregando setup_wifi.py")
    import setup_wifi
    
elif sta.active() and sta.isconnected():
    # Modo STA - Carregar dashboard
    print("[MAIN] Modo STA detectado → Carregando dashboard.py")
    import dashboard
    
else:
    print("[MAIN] ⚠️ Nenhuma interface ativa! Reiniciando...")
    import machine
    import time
    time.sleep(2)
    machine.reset()
