"""
Boot - Monitor Miner v2.0
Inicialização limpa do WiFi AP
"""

import network
import time
import gc

print("[BOOT] ========================================")
print("[BOOT] Monitor Miner v2.0 - Iniciando...")
print("[BOOT] ========================================")

# Variável global
ap_mode = False

# PASSO 1: DESLIGAR TUDO (CRÍTICO!)
print("[BOOT] [1/7] Desligando todas as interfaces...")

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

# Desconectar e desativar STA
if sta.active():
    print("[BOOT]   STA ativo, desligando...")
    sta.disconnect()
    sta.active(False)
    time.sleep(1)

# Desativar AP anterior
if ap.active():
    print("[BOOT]   AP ativo, desligando...")
    ap.active(False)
    time.sleep(1)

print("[BOOT]   ✅ Interfaces desligadas")

# PASSO 2: Limpar memória
print("[BOOT] [2/7] Limpando memória...")
gc.collect()
print(f"[BOOT]   Memória livre: {gc.mem_free()} bytes")

# PASSO 3: Aguardar estabilização
print("[BOOT] [3/7] Aguardando estabilização do WiFi...")
time.sleep(2)

# PASSO 4: Ativar AP
print("[BOOT] [4/7] Ativando Access Point...")
ap.active(True)
time.sleep(1)

# Verificar se ativou
if not ap.active():
    print("[BOOT] ❌ ERRO: AP não ativou!")
    ap_mode = False
else:
    # PASSO 5: Configurar IP
    print("[BOOT] [5/7] Configurando rede...")
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    time.sleep(0.5)
    
    # PASSO 6: Configurar SSID e segurança
    print("[BOOT] [6/7] Configurando SSID...")
    ap.config(essid='MonitorMiner_Setup', authmode=0)  # authmode=0 = Open
    time.sleep(1)
    
    # PASSO 7: Verificar
    print("[BOOT] [7/7] Verificando configuração...")
    ip_info = ap.ifconfig()
    
    print("=" * 40)
    print("[BOOT] ✅ AP ATIVO E ESTÁVEL!")
    print("=" * 40)
    print(f"[BOOT] SSID: MonitorMiner_Setup")
    print(f"[BOOT] IP: {ip_info[0]}")
    print(f"[BOOT] Gateway: {ip_info[2]}")
    print(f"[BOOT] DHCP: 192.168.4.2 - 192.168.4.254")
    print("=" * 40)
    print("[BOOT] 📱 CONECTE:")
    print("[BOOT]   WiFi: MonitorMiner_Setup (sem senha)")
    print("[BOOT]   URL: http://192.168.4.1:8080")
    print("=" * 40)
    
    ap_mode = True

print("[BOOT] Boot finalizado!")
print("[BOOT] ========================================")
