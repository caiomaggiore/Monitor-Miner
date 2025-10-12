"""
Monitor Miner v2.0 - Versão Simplificada
Servidor web básico com Microdot
"""

from microdot import Microdot
import uasyncio as asyncio
import gc

# Importar boot para verificar modo
import boot

print("[MAIN] Iniciando servidor web...")

# Criar app
app = Microdot()

# ============================================================================
# ROTAS
# ============================================================================

@app.route('/')
async def index(request):
    """Página principal"""
    print(f"[WEB] Requisição: {request.path}")
    
    html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor Miner v2.0</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-transform: uppercase;
        }
        p {
            font-size: 1.2em;
            margin-bottom: 30px;
        }
        .status {
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .api-link {
            display: inline-block;
            margin: 10px;
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 5px;
            text-decoration: none;
            color: white;
            transition: all 0.3s;
        }
        .api-link:hover {
            background: rgba(255, 255, 255, 0.5);
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Hello World!</h1>
        <p>Monitor Miner v2.0</p>
        <div class="status">
            <p>✅ Servidor ESP32 funcionando!</p>
            <p>Modo: """ + ("AP (Configuração)" if boot.ap_mode else "Normal") + """</p>
            <p>Memória livre: """ + str(gc.mem_free()) + """ bytes</p>
        </div>
        <div style="margin-top: 30px;">
            <a href="/test" class="api-link">🔍 Teste API</a>
            <a href="/api/status" class="api-link">📊 Status</a>
        </div>
    </div>
</body>
</html>
    """
    
    return html, 200, {'Content-Type': 'text/html'}

@app.route('/test')
async def test(request):
    """Rota de teste JSON"""
    print("[API] Teste acessado")
    return {
        'status': 'ok',
        'message': 'Servidor funcionando!',
        'mode': 'AP' if boot.ap_mode else 'Normal',
        'memory_free': gc.mem_free()
    }

@app.route('/api/status')
async def status(request):
    """Status do sistema"""
    print("[API] Status acessado")
    
    import network
    wlan = network.WLAN(network.AP_IF if boot.ap_mode else network.STA_IF)
    
    data = {
        'version': '2.0',
        'mode': 'AP' if boot.ap_mode else 'Normal',
        'memory_free': gc.mem_free(),
        'ip': wlan.ifconfig()[0] if wlan.active() else 'N/A'
    }
    
    return data

# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Função principal simplificada"""
    print("[MAIN] === Monitor Miner v2.0 ===")
    print(f"[MAIN] Memória livre: {gc.mem_free()} bytes")
    
    # Modo de operação
    if boot.ap_mode:
        print("[MAIN] Modo: AP (Configuração)")
        print("[MAIN] Conecte-se ao WiFi: MonitorMiner_Setup")
        print("[MAIN] Depois acesse: http://192.168.4.1:8080")
    else:
        print("[MAIN] Modo: Normal")
    
    # Liberar memória
    gc.collect()
    print(f"[MAIN] Memória após coleta: {gc.mem_free()} bytes")
    
    # Iniciar servidor HTTP primeiro
    port = 8080
    print(f"[MAIN] Iniciando servidor HTTP na porta {port}...")
    
    # Criar tarefa do servidor
    async def run_server():
        try:
            await app.start_server(port=port, debug=False)
        except Exception as e:
            print(f"[ERROR] Servidor HTTP falhou: {e}")
            import sys
            sys.print_exception(e)
    
    # Iniciar servidor em background
    asyncio.create_task(run_server())
    
    # Aguardar servidor estabilizar
    await asyncio.sleep(3)
    print("[MAIN] ✅ Servidor HTTP estável!")
    
    # Captive Portal DESABILITADO (causa problemas de conexão WiFi)
    # Usuário precisa acessar manualmente: http://192.168.4.1:8080
    
    # Loop principal para manter sistema rodando
    print("[MAIN] ========================================")
    print("[MAIN] ✅ SISTEMA PRONTO!")
    print("[MAIN] ========================================")
    
    if boot.ap_mode:
        print("[MAIN] 🔌 Conecte WiFi: MonitorMiner_Setup")
        print("[MAIN] 🌐 Acesse: http://192.168.4.1:8080")
    
    print("[MAIN] ========================================")
    
    # Loop de manutenção
    while True:
        await asyncio.sleep(30)
        gc.collect()
        # Opcional: logar memória periodicamente
        # print(f"[MAIN] Memória livre: {gc.mem_free()} bytes")

# Executar
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[MAIN] Servidor finalizado")
    except Exception as e:
        print(f"[ERROR] Erro fatal: {e}")
