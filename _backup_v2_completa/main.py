"""
Monitor Miner v2.0 - Backend API REST
ESP32 + MicroPython
"""

from microdot import Microdot, Response, send_file
import uasyncio as asyncio
import json
import time
import gc

# Importar módulos customizados
from hardware.sensors import SensorManager
from hardware.relays import RelayController
from services.logger import Logger
from services.database import Database
import boot  # Para verificar se está em AP mode

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

app = Microdot()
Response.default_content_type = 'application/json'

# Instanciar serviços essenciais
logger = Logger()
db = Database()

# Variáveis globais
boot_time = time.time()

# Inicializar hardware apenas se não estiver em AP mode
sensor_manager = None
relay_controller = None

logger.info("Sistema iniciando...")

# Aguardar um momento após boot
time.sleep(1)
gc.collect()

# Inicializar hardware de forma segura
if not boot.ap_mode:
    # Modo normal - inicializar tudo
    try:
        logger.info("Inicializando hardware completo...")
        sensor_manager = SensorManager()
        relay_controller = RelayController()
        logger.info("Hardware inicializado!")
    except Exception as e:
        logger.warning(f"Hardware não inicializado: {e}")
        sensor_manager = None
        relay_controller = None
else:
    # Modo AP - NÃO inicializar hardware
    logger.info("Modo AP - Hardware DESATIVADO (economia de memória)")
    sensor_manager = None
    relay_controller = None

# ============================================================================
# MIDDLEWARE
# ============================================================================

@app.before_request
async def before_request(request):
    """Middleware executado antes de cada requisição"""
    request.start_time = time.ticks_ms()
    return None

@app.after_request
async def after_request(request, response):
    """Middleware executado após cada requisição"""
    # Log de requisição
    duration = time.ticks_diff(time.ticks_ms(), request.start_time)
    logger.debug(f"{request.method} {request.path} - {response.status_code} ({duration}ms)")
    
    # Headers CORS (opcional)
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    return response

# ============================================================================
# API - SENSORES
# ============================================================================

@app.route('/api/sensors', methods=['GET'])
async def get_sensors(request):
    """Retorna dados de todos os sensores"""
    try:
        # Verificar se sensores estão disponíveis
        if not sensor_manager:
            return json.dumps({'error': 'Sensores não disponíveis em modo AP'}), 503
        
        data = {
            'temperature': sensor_manager.get_temperature(),
            'humidity': sensor_manager.get_humidity(),
            'current': sensor_manager.get_current(),
            'timestamp': time.time()
        }
        return json.dumps(data), 200
    except Exception as e:
        logger.error(f"Erro ao buscar sensores: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/sensors/<sensor_type>', methods=['GET'])
async def get_sensor_type(request, sensor_type):
    """Retorna dados de um tipo específico de sensor"""
    try:
        if sensor_type == 'temperature':
            data = sensor_manager.get_temperature()
        elif sensor_type == 'humidity':
            data = sensor_manager.get_humidity()
        elif sensor_type == 'current':
            data = sensor_manager.get_current()
        else:
            return json.dumps({'error': 'Invalid sensor type'}), 400
        
        return json.dumps(data), 200
    except Exception as e:
        logger.error(f"Erro ao buscar sensor {sensor_type}: {e}")
        return json.dumps({'error': str(e)}), 500

# ============================================================================
# API - RELÉS
# ============================================================================

@app.route('/api/relays', methods=['GET'])
async def get_relays(request):
    """Retorna estado de todos os relés"""
    try:
        # Verificar se relés estão disponíveis
        if not relay_controller:
            return json.dumps({'error': 'Relés não disponíveis em modo AP'}), 503
        
        data = relay_controller.get_all_states()
        return json.dumps(data), 200
    except Exception as e:
        logger.error(f"Erro ao buscar relés: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/relays/<int:relay_id>', methods=['GET'])
async def get_relay(request, relay_id):
    """Retorna estado de um relé específico"""
    try:
        if relay_id < 0 or relay_id > 3:
            return json.dumps({'error': 'Invalid relay ID'}), 400
        
        state = relay_controller.get_state(relay_id)
        data = {
            'relay_id': relay_id,
            'state': state,
            'uptime': relay_controller.get_uptime(relay_id)
        }
        return json.dumps(data), 200
    except Exception as e:
        logger.error(f"Erro ao buscar relé {relay_id}: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/relays/<int:relay_id>', methods=['POST'])
async def control_relay(request, relay_id):
    """Controla um relé"""
    try:
        if relay_id < 0 or relay_id > 3:
            return json.dumps({'error': 'Invalid relay ID'}), 400
        
        body = json.loads(request.body.decode())
        action = body.get('action', 'toggle')
        
        if action == 'on':
            relay_controller.turn_on(relay_id)
        elif action == 'off':
            relay_controller.turn_off(relay_id)
        elif action == 'toggle':
            relay_controller.toggle(relay_id)
        else:
            return json.dumps({'error': 'Invalid action'}), 400
        
        logger.info(f"Relé {relay_id} - ação: {action}")
        
        data = {
            'relay_id': relay_id,
            'state': relay_controller.get_state(relay_id),
            'action': action
        }
        return json.dumps(data), 200
    except Exception as e:
        logger.error(f"Erro ao controlar relé {relay_id}: {e}")
        return json.dumps({'error': str(e)}), 500

# ============================================================================
# API - CONFIGURAÇÃO
# ============================================================================

@app.route('/api/config', methods=['GET'])
async def get_config(request):
    """Retorna configuração completa"""
    try:
        config = db.load('config')
        return json.dumps(config), 200
    except Exception as e:
        logger.error(f"Erro ao buscar config: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/config', methods=['POST'])
async def update_config(request):
    """Atualiza configuração"""
    try:
        new_config = json.loads(request.body.decode())
        db.save('config', new_config)
        logger.info("Configuração atualizada")
        return json.dumps({'success': True}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar config: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/config/wifi', methods=['GET'])
async def get_wifi_config(request):
    """Retorna configuração WiFi"""
    try:
        config = db.load('config')
        wifi = config.get('wifi', {})
        # Remover senha por segurança
        wifi.pop('password', None)
        return json.dumps(wifi), 200
    except Exception as e:
        logger.error(f"Erro ao buscar config WiFi: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/config/wifi', methods=['POST'])
async def update_wifi_config(request):
    """Atualiza configuração WiFi"""
    try:
        wifi_config = json.loads(request.body.decode())
        config = db.load('config')
        # Merge dicionários (compatível com MicroPython)
        current_wifi = config.get('wifi', {})
        current_wifi.update(wifi_config)
        config['wifi'] = current_wifi
        db.save('config', config)
        logger.info("Configuração WiFi atualizada")
        return json.dumps({'success': True, 'message': 'Reinicie para aplicar'}), 200
    except Exception as e:
        logger.error(f"Erro ao atualizar config WiFi: {e}")
        return json.dumps({'error': str(e)}), 500

# ============================================================================
# API - WIFI SETUP (AP MODE)
# ============================================================================

@app.route('/api/wifi/scan', methods=['GET'])
async def wifi_scan(request):
    """Escaneia redes WiFi disponíveis"""
    try:
        import network
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        
        logger.info("Escaneando redes WiFi...")
        networks = sta.scan()
        
        # Formatar resultado
        result = []
        for net in networks:
            ssid = net[0].decode('utf-8')
            rssi = net[3]
            # Evitar redes vazias ou ocultas
            if ssid:
                result.append({
                    'ssid': ssid,
                    'rssi': rssi,
                    'security': net[4]
                })
        
        # Ordenar por força do sinal
        result.sort(key=lambda x: x['rssi'], reverse=True)
        
        logger.info(f"Encontradas {len(result)} redes")
        return json.dumps(result), 200
        
    except Exception as e:
        logger.error(f"Erro ao escanear WiFi: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/wifi/config', methods=['POST'])
async def save_wifi_config(request):
    """Salva configuração WiFi e reinicia"""
    try:
        data = json.loads(request.body.decode())
        ssid = data.get('ssid')
        password = data.get('password', '')
        
        if not ssid:
            return json.dumps({'success': False, 'message': 'SSID obrigatório'}), 400
        
        # Carregar config atual ou criar nova
        try:
            config = db.load('config')
        except:
            config = {}
        
        # Atualizar WiFi
        config['wifi'] = {
            'ssid': ssid,
            'password': password,
            'use_dhcp': True
        }
        
        # Salvar
        db.save('config', config)
        logger.info(f"WiFi configurado: {ssid}")
        
        # Agendar reinicialização
        async def restart_delayed():
            await asyncio.sleep(2)
            import machine
            machine.reset()
        
        asyncio.create_task(restart_delayed())
        
        return json.dumps({'success': True, 'message': 'Configuração salva, reiniciando...'}), 200
        
    except Exception as e:
        logger.error(f"Erro ao salvar WiFi: {e}")
        return json.dumps({'success': False, 'message': str(e)}), 500

# ============================================================================
# API - SISTEMA
# ============================================================================

@app.route('/api/system/status', methods=['GET'])
async def get_system_status(request):
    """Retorna status do sistema"""
    try:
        import network
        wlan = network.WLAN(network.STA_IF)
        
        data = {
            'uptime': time.time() - boot_time,
            'free_memory': gc.mem_free(),
            'wifi': {
                'connected': wlan.isconnected(),
                'ip': wlan.ifconfig()[0] if wlan.isconnected() else None,
                'rssi': wlan.status('rssi') if wlan.isconnected() else None
            },
            'version': '2.0.0'
        }
        return json.dumps(data), 200
    except Exception as e:
        logger.error(f"Erro ao buscar status: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/system/logs', methods=['GET'])
async def get_logs(request):
    """Retorna logs do sistema"""
    try:
        limit = int(request.args.get('limit', 50))
        logs = logger.get_recent(limit)
        return json.dumps(logs), 200
    except Exception as e:
        logger.error(f"Erro ao buscar logs: {e}")
        return json.dumps({'error': str(e)}), 500

@app.route('/api/system/ping', methods=['GET'])
async def ping(request):
    """Ping para teste de conectividade"""
    return json.dumps({'pong': True, 'timestamp': time.time()}), 200

@app.route('/api/system/restart', methods=['POST'])
async def restart_system(request):
    """Reinicia o sistema"""
    try:
        logger.warning("Sistema reiniciando por requisição API")
        await asyncio.sleep(1)
        import machine
        machine.reset()
    except Exception as e:
        logger.error(f"Erro ao reiniciar: {e}")
        return json.dumps({'error': str(e)}), 500

# ============================================================================
# SERVIR ARQUIVOS ESTÁTICOS (Frontend)
# ============================================================================

@app.route('/')
async def serve_index(request):
    """Serve index.html ou setup.html dependendo do modo"""
    logger.info(f"Requisição: {request.method} {request.path}")
    
    try:
        # Se estiver em AP mode, servir página de configuração
        if boot.ap_mode:
            logger.info("Servindo setup.html (modo AP)")
            # Ler arquivo manualmente
            with open('web/setup.html', 'r') as f:
                html = f.read()
            return html, 200, {'Content-Type': 'text/html'}
        
        logger.info("Servindo index.html (modo normal)")
        # Ler arquivo manualmente
        with open('web/index.html', 'r') as f:
            html = f.read()
        return html, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        logger.error(f"Erro ao servir HTML: {e}")
        return f'<h1>Monitor Miner v2.0</h1><p>Erro: {e}</p>', 500, {'Content-Type': 'text/html'}

@app.route('/test')
async def test_route(request):
    """Rota de teste simples"""
    logger.info("Rota /test acessada!")
    return {'status': 'ok', 'message': 'Servidor funcionando!', 'mode': 'AP' if boot.ap_mode else 'Normal'}, 200

@app.route('/static/<path:path>')
async def serve_static(request, path):
    """Serve arquivos estáticos"""
    if '..' in path:
        return 'Not found', 404
    
    # Determinar content type
    content_type = 'text/plain'
    if path.endswith('.html'):
        content_type = 'text/html'
    elif path.endswith('.css'):
        content_type = 'text/css'
    elif path.endswith('.js'):
        content_type = 'application/javascript'
    elif path.endswith('.json'):
        content_type = 'application/json'
    elif path.endswith('.png'):
        content_type = 'image/png'
    elif path.endswith('.jpg') or path.endswith('.jpeg'):
        content_type = 'image/jpeg'
    elif path.endswith('.svg'):
        content_type = 'image/svg+xml'
    
    try:
        return send_file(f'web/{path}', content_type=content_type)
    except:
        return 'Not found', 404

# ============================================================================
# ERRO 404
# ============================================================================

@app.errorhandler(404)
async def not_found(request):
    """Handler para 404"""
    return json.dumps({'error': 'Not found'}), 404

# ============================================================================
# TAREFAS EM BACKGROUND
# ============================================================================

async def sensor_reading_task():
    """Tarefa para leitura contínua dos sensores"""
    logger.info("Iniciando tarefa de leitura de sensores")
    
    while True:
        try:
            await sensor_manager.read_all()
            await asyncio.sleep(5)  # Ler a cada 5 segundos
        except Exception as e:
            logger.error(f"Erro na leitura de sensores: {e}")
            await asyncio.sleep(10)

async def automation_task():
    """Tarefa para automação (ligar/desligar relés baseado em sensores)"""
    logger.info("Iniciando tarefa de automação")
    
    while True:
        try:
            # Implementar lógica de automação aqui
            # Exemplo: ligar ventilador se temperatura > 30°C
            await asyncio.sleep(30)  # Verificar a cada 30 segundos
        except Exception as e:
            logger.error(f"Erro na automação: {e}")
            await asyncio.sleep(60)

# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Função principal"""
    try:
        logger.info("=== Monitor Miner v2.0 ===")
        logger.info("Iniciando sistema...")
        
        # Garbage collection
        gc.collect()
        logger.info(f"Memória livre: {gc.mem_free()} bytes")
        
        # Verificar modo de operação
        if boot.ap_mode:
            # Modo AP (Configuração) - APENAS servidor web
            logger.info("Modo: AP (Configuração)")
            logger.info("Iniciando servidor HTTP leve na porta 80...")
            logger.info("Sensores e automação DESATIVADOS em modo configuração")
        else:
            # Modo Normal - Sistema completo
            logger.info("Modo: Normal (Produção)")
            logger.info("Iniciando tarefas em background...")
            
            # Iniciar tarefas apenas em modo normal
            asyncio.create_task(sensor_reading_task())
            asyncio.create_task(automation_task())
            logger.info("Tarefas iniciadas: Sensores + Automação")
        
        # Iniciar servidor HTTP (em ambos os modos)
        port = 8080  # Usar porta 8080 (mais compatível)
        logger.info(f"Iniciando servidor HTTP na porta {port}...")
        
        if boot.ap_mode:
            logger.info(f"Acesse: http://192.168.4.1:{port}")
        
        logger.info("Servidor iniciando...")
        await app.start_server(port=port, debug=True)  # Debug ativo para ver logs
        
    except Exception as e:
        logger.critical(f"Erro crítico no main: {e}")
        import sys
        sys.print_exception(e)
        
        logger.info("Reiniciando em 10 segundos...")
        await asyncio.sleep(10)
        import machine
        machine.reset()

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Sistema finalizado por usuário")
    except Exception as e:
        logger.critical(f"Erro fatal: {e}")

