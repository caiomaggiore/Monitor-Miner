"""
Boot - Inicialização do sistema
Conecta ao WiFi ou abre AP mode para configuração
"""

import network
import time
from services.logger import Logger
from services.database import Database

logger = Logger()
db = Database()

# Variável global para indicar modo AP
ap_mode = False

def start_ap_mode():
    """Inicia modo Access Point para configuração"""
    global ap_mode
    logger.info("Iniciando modo AP (Configuração WiFi)...")
    
    # Desativar STA
    sta = network.WLAN(network.STA_IF)
    sta.active(False)
    
    # Ativar AP
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    
    # Configurar IP do AP ANTES de configurar o ESSID
    # Isso garante que o DHCP funcione corretamente
    ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    
    # Configurar AP (ESSID e senha)
    ap.config(essid='MonitorMiner_Setup')
    ap.config(password='')  # Sem senha
    ap.config(authmode=network.AUTH_OPEN)  # Modo aberto (sem senha)
    ap.config(max_clients=4)  # Máximo 4 clientes
    
    # Aguardar AP estar ativo
    max_wait = 10
    while not ap.active() and max_wait > 0:
        time.sleep(0.5)
        max_wait -= 1
    
    if not ap.active():
        logger.error("Falha ao ativar AP!")
        return False
    
    # Verificar configuração
    ip_info = ap.ifconfig()
    logger.info(f"AP ativo! SSID: MonitorMiner_Setup")
    logger.info(f"IP do AP: {ip_info[0]}")
    logger.info(f"Gateway: {ip_info[2]}")
    logger.info(f"Máscara: {ip_info[1]}")
    logger.info("=" * 40)
    logger.info("CONECTE-SE:")
    logger.info("  1. WiFi: MonitorMiner_Setup")
    logger.info("  2. Acesse: http://192.168.4.1:8080")
    logger.info("  3. Ou teste: http://192.168.4.1:8080/test")
    logger.info("=" * 40)
    logger.info("DHCP ativo: clientes receberão IP 192.168.4.x automaticamente")
    
    ap_mode = True
    return True

def connect_wifi():
    """Conecta ao WiFi"""
    logger.info("Iniciando conexão WiFi...")
    
    # Desabilitar AP mode primeiro
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    
    # Carregar configuração
    try:
        config = db.load('config')
        wifi_config = config.get('wifi', {})
        ssid = wifi_config.get('ssid', '')
        password = wifi_config.get('password', '')
        
        # Se não houver SSID configurado, ir direto para AP mode
        if not ssid or ssid == 'SuaRede':
            logger.warning("WiFi não configurado - iniciando AP mode")
            return start_ap_mode()
            
    except:
        logger.warning("Configuração não encontrada - iniciando AP mode")
        return start_ap_mode()
    
    # Configurar interface STA
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # IP estático ou DHCP
    if not wifi_config.get('use_dhcp', True):
        ip = wifi_config.get('static_ip', '192.168.1.100')
        mask = wifi_config.get('subnet_mask', '255.255.255.0')
        gateway = wifi_config.get('gateway', '192.168.1.1')
        dns = wifi_config.get('dns', '8.8.8.8')
        wlan.ifconfig((ip, mask, gateway, dns))
        logger.info(f"IP estático configurado: {ip}")
    
    # Conectar
    if not wlan.isconnected():
        logger.info(f"Conectando a: {ssid}")
        wlan.connect(ssid, password)
        
        # Aguardar conexão (timeout 15s)
        timeout = 15
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > timeout:
                logger.error(f"Timeout ao conectar WiFi: {ssid}")
                logger.info("Iniciando AP mode para reconfiguração...")
                return start_ap_mode()
            time.sleep(0.5)
    
    # Sucesso
    ip_info = wlan.ifconfig()
    logger.info(f"WiFi conectado! IP: {ip_info[0]}")
    logger.info(f"RSSI: {wlan.status('rssi')} dBm")
    
    return True

def configure_system():
    """Configura sistema"""
    logger.info("Configurando sistema...")
    
    # Garbage collection
    import gc
    gc.enable()
    gc.collect()
    logger.info(f"Memória livre: {gc.mem_free()} bytes")

# ============================================================================
# EXECUTAR BOOT
# ============================================================================

logger.info("=== BOOT ===")
logger.info("Monitor Miner v2.0")

# Configurar sistema
configure_system()

# Conectar WiFi ou iniciar AP mode
connect_wifi()

logger.info("Boot completo!")
logger.info("=" * 40)

